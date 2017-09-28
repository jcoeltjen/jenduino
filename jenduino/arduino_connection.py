import logging
from serial import Serial

LOGGER = logging.getLogger('ArduinoConnection')


class ArduinoConnection:
    BLUE = 0xe0
    BLUE_ANIME = 0xe1
    RED = 0xe2
    RED_ANIME = 0xe3
    DELIMITER = 0xFF

    def __init__(self, com_port, baud_rate) -> None:
        self.com_port = com_port
        self.baud_rate = baud_rate

    def convert_data(self, job_statuses):
        """Converts the given statues and IDs to raw byte values that
        can be transferred using the write_serial() function."""
        LOGGER.info('Start converting data...')
        send_bytes = list()
        for job_status in job_statuses:
            if job_status['status'] == 'blue':
                send_bytes.append(self.BLUE)
            if job_status['status'] == 'blue_anime':
                send_bytes.append(self.BLUE_ANIME)
            if job_status['status'] == 'red':
                send_bytes.append(self.RED)
            if job_status['status'] == 'red_anime':
                send_bytes.append(self.RED_ANIME)
            send_bytes.append(self.DELIMITER)
        return send_bytes

    def write_serial(self, send_data):
        LOGGER.info('Begin writing to serial port %s with baudrate %s' % (self.com_port, self.baud_rate))
        ser = Serial()
        ser.baudrate = self.baud_rate
        ser.port = self.com_port
        ser.open()
        # TODO wait until device ready
        send_bytes = bytes(send_data)
        logging.info('Sending this: {}'.format(send_bytes))
        ser.write(data=send_bytes)
        ser.close()
