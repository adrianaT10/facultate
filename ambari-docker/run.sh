#!/usr/bin/env bash

NODE_NAME_PREFIX="ambari"
let N=3
let PORT=8080
let S=0

function usage() {
    echo "Usage: ./run.sh [--nodes=3] [--port=8080] [--secure]"
    echo
    echo "--nodes      Specify the number of total nodes"
    echo "--port       Specify the port of your local machine to access Ambari Web UI (8080 - 8088)"
    echo "--secure     Specify the cluster to be secure"
}

# Parse and validate the command line arguments
function parse_arguments() {
    while [ "$1" != "" ]; do
        PARAM=`echo $1 | awk -F= '{print $1}'`
        VALUE=`echo $1 | awk -F= '{print $2}'`
        case $PARAM in
            -h | --help)
                usage
                exit
                ;;
            --port)
                PORT=$VALUE
                ;;
            --nodes)
                N=$VALUE
                ;;
            --secure)
                S=1
                ;;
            *)
                echo "ERROR: unknown parameter \"$PARAM\""
                usage
                exit 1
                ;;
        esac
        shift
    done
}

parse_arguments $@

docker build -t ambari .
docker network create ambari-net 2> /dev/null

# remove the outdated master
docker rm -f $(docker ps -a -q -f "name=$NODE_NAME_PREFIX") 2>&1 > /dev/null

# launch containers
master_id=$(docker run -d --net ambari-net -p $PORT:8080 -p 6080:6080 -p 9090:9090 -p 9000:9000 -p 2181:2181 -p 8000:8000 -p 8020:8020 -p 42111:42111 -p 10500:10500 -p 16030:16030 -p 8042:8042 -p 8040:8040 -p 2100:2100 -p 4200:4200 -p 4040:4040 -p 8050:8050 -p 9996:9996 -p 9995:9995 -p 8088:8088 -p 8886:8886 -p 8889:8889 -p 8443:8443 -p 8744:8744 -p 8888:8888 -p 8188:8188 -p 8983:8983 -p 1000:1000 -p 1100:1100 -p 11000:11000 -p 10001:10001 -p 15000:15000 -p 10000:10000 -p 8993:8993 -p 1988:1988 -p 5007:5007 -p 50070:50070 -p 19888:19888 -p 16010:16010 -p 50111:50111 -p 50075:50075 -p 18080:18080 -p 60000:60000 -p 8090:8090 -p 8091:8091 -p 8006:8005 -p 8086:8086 -p 8082:8082 -p 60080:60080 -p 8765:8765 -p 5011:5011 -p 6001:6001 -p 6003:6003 -p 6008:6008 -p 1220:1220 -p 21000:21000 -p 6188:6188 -p 2222:22 -p 50010:50010 -p 6667:6667 -p 3000:3000 --privileged=true --name $NODE_NAME_PREFIX-0 ambari)
echo ${master_id:0:12} > hosts
for i in $(seq $((N-1)));
do
    container_id=$(docker run -d --net ambari-net --privileged=true --name $NODE_NAME_PREFIX-$i ambari)
    echo ${container_id:0:12} >> hosts
done

# Copy the workers file to the master container
docker cp hosts $master_id:/root
# print the hostnames
echo "Using the following hostnames:"
echo "------------------------------"
cat hosts
echo "------------------------------"

# print the private key
echo "Copying back the private key..."
docker cp $master_id:/root/.ssh/id_rsa .

# the following functionality (run in secure mode) is IN PROGRESS
if [ $S -eq 1 ]; then
    echo '
#!/bin/sh

echo "Installing Kerberos"
yum install -y krb5-server krb5-libs krb5-workstation

echo "Using default configuration"
REALM="EXAMPLE.COM"

HOSTNAME=`hostname`
cat >/etc/krb5.conf <<EOF
[logging]
    default = FILE:/var/log/krb5libs.log
    kdc = FILE:/var/log/krb5kdc.log
    admin_server = FILE:/var/log/kadmind.log

[libdefaults]
    default_realm = ${REALM}
    dns_lookup_realm = false
    dns_lookup_kdc = false
    ticket_lifetime = 24h
    renew_lifetime = 7d
    forwardable = true

[realms]
    ${REALM} = {
        kdc = ${HOSTNAME}
        admin_server = ${HOSTNAME}
    }

[domain_realm]
    .${HOSTNAME} = ${REALM}
    ${HOSTNAME} = ${REALM}
EOF

echo "Creating kadm5.acl file"
cat >/var/kerberos/krb5kdc/kadm5.acl <<EOF
*/admin@${REALM}    *
EOF

echo "Creating KDC database"
kdb5_util create -s -P hadoop

echo "Creating administriative account. Principal: admin/admin. Password: ambari"
kadmin.local -q "addprinc -pw ambari admin/admin"

echo "Starting services"
service krb5kdc start
service kadmin start

chkconfig krb5kdc on
chkconfig kadmin on' >> install_Kerberos.sh

    # Copy the Kerberos installation script to the master container
    echo "Copying the Kerberos installation script..."
    docker cp install_Kerberos.sh $master_id:/root

fi

# Start the ambari server
docker exec $NODE_NAME_PREFIX-0 ambari-server start
