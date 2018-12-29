

import requests
import json
import sys


AMBARI_DOMAIN = '127.0.0.1'
AMBARI_PORT = '8089'
AMBARI_USER = 'admin'
AMBARI_PSW = 'admin'

authPair = (AMBARI_USER, AMBARI_PSW)

HOST_1 = "aa22653ec978"
HOST_2 = "b758fd61d913"
HOST_3 = "1a9e99e252e4"

RM = HOST_3
NM = [HOST_2, HOST_3]

NAMENODE = HOST_1
DATANODES = [HOST_1, HOST_2, HOST_3]


def ambariRequest( method, restAPI ):
	url = "http://" + AMBARI_DOMAIN + ":" + AMBARI_PORT + restAPI
	headers = {'X-Requested-By': 'darya'}
	r = requests.request(method, url, auth=authPair, headers=headers)
	print(r)
	# return json.loads(r.text)
	return r.text

def ambariRequestJSON( method, restAPI, json_obj ):
	url = "http://" + AMBARI_DOMAIN + ":" + AMBARI_PORT + restAPI
	headers = {'X-Requested-By': 'darya'}
	r = requests.request(method, url, auth=authPair, headers=headers, json=json_obj)
	print(r)
	# return json.loads(r.text)
	return r.text

def getAmbariHosts():
	restAPI = "/api/v1/hosts"
	return ambariRest(restAPI)

def deleteHostComponent(host, component):
	res = ambariRequest('DELETE', '/api/v1/clusters/dockercluster/hosts/' + host + '/host_components/' + component)
	print(res)



def stopNodeManager(host):
	body = {'HostRoles': {'state': 'INSTALLED'}}
	res = ambariRequestJSON('PUT', '/api/v1/clusters/dockercluster/hosts/hostname/' + host + '/NODEMANAGER', json.dumps(body, separators=(',',':')))
	print(res)


if __name__ == '__main__':
	deleteHostComponent(HOST_3, 'MAPREDUCE2_CLIENT')
	# stopNodeManager(HOST_3)
	

