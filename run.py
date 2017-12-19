from crossover_remote_stat.app.xml_handler import XMLHandler
from crossover_remote_stat import server, config

# get port from config file
PORT = int(config['SERVER']['PORT'])

# add new clients into xml file to db

clients = XMLHandler.get_clients()
was_initialized = server.save_clients(clients)
if was_initialized:
	server.upload_client(clients)

# run http rest flask server
# server.app.run(debug=True,port=PORT)
