import json
import logging

from jenkinsapi.jenkins import Jenkins
from serial import Serial

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

config = json.load(open('config.json'))
jobs = json.load(open('jobs.json'))

BLUE = 0xe0
BLUE_ANIME = 0xe1
RED = 0xe2
RED_ANIME = 0xe3
DELIMITER = 0xFF

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

def convert_data(job_statuses):
    """Converts the given statues and IDs to raw byte values that can be transferred using the write_serial() function."""
    logging.info('Start converting data...')
    send_bytes = list()
    for job_status in job_statuses:
        send_bytes.append(job_status['id'])
        if job_status['status'] == 'blue':
            send_bytes.append(BLUE)
        if job_status['status'] == 'blue_anime':
            send_bytes.append(BLUE_ANIME)
        if job_status['status'] == 'red':
            send_bytes.append(RED)
        if job_status['status'] == 'red_anime':
            send_bytes.append(RED_ANIME)
        send_bytes.append(DELIMITER)
    return send_bytes


def main():
    jenkins = create_jenkins_object()
    job_statuses = load_job_stati(jenkins=jenkins)
    logging.info('job stati: {}'.format(job_statuses))
    send_data = convert_data(job_statuses)
    logging.info('send data: {}'.format(send_data))
    write_serial(send_data)


if __name__ == '__main__':
    main()
