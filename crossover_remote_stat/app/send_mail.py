from smtplib import SMTP
from crossover_remote_stat import config

MAIL_CONFIG = dict(config._sections['DATABASE'])

def send_mail(to, message):

	server = SMTP(MAIL_CONFIG['host'])
	# I dont know if you may need this setting
	server.starttls()
	# ... or this one
	server.login(MAIL_CONFIG['user'],MAIL_CONFIG['pass'])

	server.sendmail(MAIL_CONFIG['host'], to, message)
	server.quit()

def send_alert(to):
	message = '''booo'''
	send_mail(to, message1)

send_alert('freddygarciaabreu@gmail.com')