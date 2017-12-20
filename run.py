from threading import Thread

from crossover_remote_stat.app.xml_handler import XMLHandler
from crossover_remote_stat import server, config

# get port from config file
PORT = int(config['SERVER']['PORT'])

# add new clients into xml file to db
# and upload the script to them
Thread(target=server.initialize).start()

# run http rest flask server
server.app.run(host='0.0.0.0',port=PORT)
