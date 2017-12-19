from crossover_remote_stat import server, config

# get port from config file
PORT = int(config['SERVER']['PORT'])

# add new clients into xml file to db
server.initialize()

# run http rest flask server
server.app.run(debug=True,port=PORT)
