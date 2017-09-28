import logging
from jenkinsapi.jenkins import Jenkins

LOGGER = logging.getLogger('JenkinsConnection')


class JenkinsConnection:
    def __init__(self, url, username, password) -> None:
        LOGGER.info('Initialize connection to %s with username %s' % (url, username))
        self.jenkins = Jenkins(url, username, password)

    def load_job_stati(self, jobs):
        return_jobs = list()
        for job in jobs:
            job_object = {
                'id': job['id'],
                'status': self.jenkins.get_job(job['name']).color
            }
            return_jobs.append(job_object)
        return return_jobs
