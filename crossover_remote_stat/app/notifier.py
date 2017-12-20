from smtplib import SMTP
from crossover_remote_stat import config

MAIL_CONFIG = dict(config._sections['MAIL'])

def send_mail(to, message, attachments=None):
	server = SMTP(MAIL_CONFIG['host'], 587)
	# I dont know if you may need this setting
	server.starttls()
	# ... or this one
	server.login(MAIL_CONFIG['user'],MAIL_CONFIG['pass'])

	server.sendmail(MAIL_CONFIG['host'], to, message)
	server.quit()

def send_alert(to, params):
	message = '''
		your pc has a high resource consumption:

		details: cpu limit level [{cpu_limit}%]
		details: cpu usage level [{cpu_percent}%]

		details: memory limit level [{memory_limit}%]
		details: memory usage level [{memory_usage}%]
	'''.format(**params)

	send_mail(to, message)

def send_win_logs(to, logs):
	message = '''

	'''
	send_mail(to, message1)

def handle_alerts(client, statistics):
	last_execution = client.execution[-1]

	memory_limit = last_execution.memory_limit
	memory_usage = float(statistics.get('memory_usage'))
	cpu_limit = last_execution.cpu_limit
	cpu_percent = float(statistics.get('cpu_percent'))

	if memory_usage > memory_limit or cpu_percent > cpu_limit :

		to = client.email
		params = {
			'cpu_limit' : cpu_limit,
			'cpu_percent' : cpu_percent,
			'memory_limit' : memory_limit,
			'memory_usage' : memory_usage
		}
		send_alert(to, params)

