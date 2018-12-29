import subprocess
import time

def get_job_id():
	job_cmd = subprocess.Popen("mapred job -list".split(), stdout=subprocess.PIPE)
	out, err = job_cmd.communicate()

	res = out.split()
	job_id = res[-12]

	if (job_id == 'State'):
		print ("No job found")
		return -1
	return job_id


def get_attempts(job_id):
	cmd = "mapred job -list-attempt-ids " + job_id + " REDUCE running"
	job_cmd = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
	out, err = job_cmd.communicate()

	attempts = out.split()

def fail_reducer(attempt):
	cmd = "mapred job -fail-task " + attempt
	job_cmd = subprocess.Popen(cmd.split())

if __name__ == '__main__':

	while True:
		job = get_job_id()
		if job == -1:
			return

		attempts = get_attempts(job)

		for attempt in attempts:
			fail_reducer(attempt)
		time.sleep(3)