from configparser import ConfigParser

CONFIG_FILENAME = './CrossOverAssignment/config.cfg'

def get_config():
	config = ConfigParser()
	config.read(CONFIG_FILENAME)
	return config

config = get_config()


