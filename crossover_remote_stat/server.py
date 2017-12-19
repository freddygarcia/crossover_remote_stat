from datetime import datetime
from cryptography.fernet import Fernet
from flask import Flask, request
from logging import getLogger
from pickle import loads as pickle_loads
from socket import socket, AF_INET, SOCK_STREAM
from crossover_remote_stat.app.database.models import Client, ScanType, \
										ScanResult, WindowsEventLog, Session 
from crossover_remote_stat.app.xml_handler import XMLHandler
from crossover_remote_stat.app.client_side.uploader import upload_and_execute


log = getLogger(__name__)
app = Flask(__name__)

def save_clients(clients):
	"""Read xml looking for client pc"""

	# get just clients ip address as a set
	clients_ip = { c.get('ip') for c in XMLHandler.get_clients() }
	# check which clients exist
	existing_clients = Session.query(Client).filter(Client.ip_address.in_(clients_ip)).all()
	# get the ip address of saved clients 
	existing_clients_ip = { x.ip_address for x in existing_clients }
	# determine which clients are new in the xml file
	new_clients_ip = clients_ip - existing_clients_ip
	# get the complete new client data
	new_clients = [ c for c in clients if c.get('ip') in new_clients_ip]

	# insert into db new clients
	for d_client in new_clients:
		client = Client.load_from_dict(d_client)
		client.token = Fernet.generate_key()
		try:
			for alert in d_client.get('alert'):
				scanresult = ScanResult()
				scanresult.scan_type_key = alert.get('type')
				scanresult.limit_value = alert.get('limit')
				scanresult.client = client
				Session.add(scanresult)
			Session.add(client)
			Session.commit()
		except Exception as e:
			print(e)
			Session.rollback()
			return False
	return True

def upload_client(clients):
	if XMLHandler.validate_xml():
		for client in clients:
			upload_and_execute(client)
	else:
		log.warning('No valid xml file')

def initialize():
	# get all clients from xml
	clients = XMLHandler.get_clients()
	clients_where_saved = save_clients(clients)

	if clients_where_saved:
		upload_client(clients)

def save_statistics(client, statistics):
	'''client = DbModel, statistics = dict'''
	client.os = statistics.get('os')
	client.hostname = statistics.get('platform')
	client.scan_date = datetime.now()

	if statistics.os == 'Windows' and statistics.event_logs is not False:
		for dc_win_event_log in statistics.event_logs :
			w_event_log = WindowsEventLog.load_from_dict()
			Session.add(w_event_log)
			try:
				Session.commit()
			except Exception as e:
				Session.rollback()

@app.route("/",methods=['GET', 'POST'])
def index():
	# if post
	if request.method == 'POST':
		# capture the incoming data
		incoming = request.data
		# get the remote host address
		remote_addr = request.remote_addr
		# check if we expected to recieve something from that ip
		client = Session.query(Client).filter(Client.ip_address == remote_addr).first()

		# if client is found
		if client is not None:
			# generate decrypter algorithm
			decrypter = Fernet(client.token)
			# proccess the decrypt the data
			d_statistics = decrypter.decrypt(incoming)
			# unpickle data
			statistics = pickle_loads(d_statistics)
			# associate statistics to client
			save_statistics(client, statistics)
			return str(statistics)

	return 'Works!'
