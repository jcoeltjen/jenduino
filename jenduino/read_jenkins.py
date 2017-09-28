import json
import logging

from jenkinsapi.jenkins import Jenkins
from serial import Serial

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

config = json.load(open('config.json'))
jobs = json.load(open('jobs.json'))


def create_jenkins_object():
    jenkins_config = config['jenkins']
    return Jenkins(baseurl=jenkins_config['url'], username=jenkins_config['username'],
                   password=jenkins_config['password'])


def load_job_stati(jenkins):
    return_jobs = list()
    for job in jobs:
        job_object = {
            'id': job['id'],
            'status': jenkins.jobs[job['name']]._data['color']
        }
        return_jobs.append(job_object)
    return return_jobs


def write_serial(send_data):
    logging.info('Begin writing to serial port {0} with baudrate {1}'.format(config['serial']['port'],
                                                                             config['serial']['baudrate']))
    ser = Serial()
    ser.baudrate = config['serial']['baudrate']
    ser.port = config['serial']['port']
    ser.open()
    # TODO wait until device ready
    send_bytes = bytes(send_data)
    logging.info('Sending this: {}'.format(send_bytes))
    ser.write(data=send_bytes)
    ser.close()




