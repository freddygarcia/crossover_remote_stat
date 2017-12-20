from datetime import datetime
from cryptography.fernet import Fernet
from flask import Flask, request
from logging import getLogger
from pickle import loads as pickle_loads
from socket import socket, AF_INET, SOCK_STREAM
from crossover_remote_stat.app.client_side.uploader import upload_and_execute
from crossover_remote_stat.app.database.models import Client, Execution, \
										Scan, WindowsEventLog, Session 

from crossover_remote_stat.app.notifier import handle_alerts
from crossover_remote_stat.app.xml_handler import XMLHandler


log = getLogger(__name__)
app = Flask(__name__)

def save_clients(clients):
	"""Read xml looking for client pc
		It also retrieve a modified list of clients with
		a key to encrypt the connection
	"""
	# insert into db new clients
	for d_client in clients:
		client = Session.query(Client).filter(Client.ip_address == d_client.get('ip')).first()

		if client is None:
			client = Client.load_from_dict(d_client)

		try:
			generated_key = Fernet.generate_key()

			execution = Execution(generated_key)
			execution.memory_limit = d_client.get('memory')
			execution.cpu_limit = d_client.get('cpu')
			client.execution.append(execution)

			d_client['token'] = generated_key 

			Session.add(client)
			Session.commit()
		except Exception as e:
			log.error('client {} couldnt be saved'.format(client.ip_address))
			log.error(e)
			Session.rollback()

	return clients

def initialize():
	if XMLHandler.validate_xml():
		# get all clients from xml
		clients = XMLHandler.get_clients()
		clients_to_upload = save_clients(clients)

		for client in clients_to_upload:
			if upload_and_execute(client):
				log.info('upload success for client [{}]'.format(client['ip']))
			else:
				log.error('couldnt upload file to client [{}]'.format(client['ip']))
	else:
		no_valid_error = 'No valid xml file'
		log.error(no_valid_error)
		raise Exception(no_valid_error)

def save_statistics(client, statistics):
	'''client = DbModel, statistics = dict'''

	if statistics.get('first_time_running'):
		client.os = statistics.get('os')
		client.uptime = statistics.get('uptime')
		client.hostname = statistics.get('hostname')
		client.execution[-1].start_date = datetime.now()	

	client.execution[-1].scan.append(Scan(statistics))
	client.execution[-1].uptime = statistics.get('uptime')

	try:
		Session.add(client)
		Session.commit()
		log.info('statistics saved!')
	except Exception as e:
		Session.rollback()
		log.error(e)
		log.error('fail saving statistics')

	if statistics.get('os') == 'Windows' and statistics.get('event_logs') is not False:
		for dc_win_event_log in statistics.get('event_logs') :
			w_event_log = WindowsEventLog.load_from_dict()
			Session.add(w_event_log)
			try:
				Session.commit()
			except Exception as e:
				Session.rollback()
				log.error(e)
				log.error('fail saving windows event logs')


@app.route("/",methods=['GET', 'POST'])
def index():
	# if post
	if request.method == 'POST':
		# capture the incoming data
		incoming = request.data
		# get the remote host address
		remote_addr = request.remote_addr
		# check if we expected to recieve something from that ip
		client = Session.query(Client).filter(Client.ip_address == remote_addr).one()
		# if client is found
		if client is not None:
			# generate decrypter algorithm
			# look for last saved token
			decrypter = Fernet(client.execution[-1].token)
			# proccess the decrypt the data
			d_statistics = decrypter.decrypt(incoming)
			# unpickle data
			statistics = pickle_loads(d_statistics)
			# associate statistics to execution
			save_statistics(client, statistics)
			handle_alerts(client, statistics)
			return str(statistics)

	return 'Works!'
