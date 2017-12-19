from configparser import ConfigParser
import logging

CONFIG_FILENAME = './crossover_remote_stat/config.cfg'

def get_config():
	config = ConfigParser()
	config.read(CONFIG_FILENAME)
	return config

config = get_config()

# get log config from general config file
# I know that could came from a logging confil file 
# but I didn't many config files and think looks elegant 
config_log = dict(config._sections['LOGGING'])
# initialize logger
logging.basicConfig(format=config_log['frmt'],filename=config_log['file']
						,level=logging.DEBUG,datefmt=config_log['date'])
