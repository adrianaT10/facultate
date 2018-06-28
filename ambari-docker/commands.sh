# /usr/hdp/current/hadoop-mapreduce-client/ aici se afla jarul!!!

yarn application -list -appStates ALL  -> get app id
yarn applicationattempt -list <Application ID> => get app attempt id
yarn container -list <app atempt id>  -> get containers
//also by rest to resource manager

curl --user admin:admin http://localhost:8089/api/v1/clusters/dockercluster/workflows

curl --user admin:admin http://localhost:8089/api/v1/clusters/dockercluster/workflows/:id

curl --user admin:admin http://localhost:8089/api/v1/clusters/dockercluster/workflows/:id/jobs/:id/taskattempts

curl --user admin:admin http://localhost:8089/api/v1/clusters/dockercluster/workflows/:id/jobs/:id/taskattempts/:id


mapred job -list
mapred job -list-attempt-ids <job_id> REDUCE running
mapred job -fail-task <attempt_id>