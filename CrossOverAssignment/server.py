from hashlib import sha1
from hmac import new as new_hmac
from flask import Flask, request
from pickle import loads as pickle_loads
from socket import socket, AF_INET, SOCK_STREAM
from uuid import uuid4
from CrossOverAssignment.app.database.models import Client, ScanType, ScanResult, Session
from CrossOverAssignment.app.xml_handler import XMLHandler

app = Flask(__name__)

def initialize():
	"""Read xml looking for client pc"""
	if XMLHandler.validate_xml():
		# get all clients from xml
		clients = XMLHandler.get_clients()
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
			client.token = str(uuid4())
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
	else:
		print('No valid xml file')
		return False

@app.route("/",methods=['GET', 'POST'])
def hello():
	if request.method == 'POST':
		incoming = request.data
		header, body = incoming.split(b' ')

		client = Session.query(Client).filter(Client.token == header).first()

		if hex_digest is not None:
			statistics = pickle_loads(body)

			# for stat in statistics.keys():
			# 	scan = ScanResult()

			return str(statistics)
	return 'a'