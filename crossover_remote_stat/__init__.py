from configparser import ConfigParser

CONFIG_FILENAME = './crossover_remote_stat/config.cfg'

def get_config():
	config = ConfigParser()
	config.read(CONFIG_FILENAME)
	return config

config = get_config()


