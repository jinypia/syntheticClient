import requests
import time
import os
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = TimedRotatingFileHandler("hcQualtrics.log", when="midnight", interval=1)
file_handler.suffix = "%Y%m%d"
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(file_handler)
#logger.addHandler(ch)

'''
Qualtrics Healthcheck
'''

url = "https://www.qualtrics.com/status/data.json"
RESTART_SH = 'echo "Test Failed"'
SLEEP_INTERVAL = 60

def healthCheckQualtrics(url):
    try:
        logger.info("start access url %s" % (url))
        response = requests.get(url, timeout=1)
        response.raise_for_status()
        if response.status_code() == 200:
            dicData = response.json()

            for data in dicData['appStatuses']:
                if data['SYD1'] != '0':
                    print(data['name'])
        else:
            logger.info("warning code:"+str(a.getcode()))
    #    json_data = json.dump(dict, dicData, indent='\t')    
    #    print(json.dumps(json_data, indent = '\t'))
        return True

    except requests.exceptions as e:
        logger.error('health check failed %s ' % (str(e)))

    logger.info("health not ok")    
    return False

#check the health for specified period
def check_periodically(url, failed_action_func):
    while True:
        try:
            time.sleep(SLEEP_INTERVAL)
            logger.info("check awake, start check")
            if not healthCheckQualtrics(url):
                failed_action_func()
        except Exception as e:
            logger.error('check periodically failed %s ' % (str(e)))
        pass

def restart_server():
    do_script(RESTART_SH)
    pass

def do_script(the_scripts):
    logger.info("=========start script %s======" % the_scripts)
    result = os.popen(the_scripts).read()
    logger.info(result)
    logger.info("=========end   script %s======" % the_scripts)
    pass

if __name__ == '__main__':
    check_periodically(url, restart_server)
    pass

