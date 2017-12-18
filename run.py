from CrossOverAssignment import server, config

PORT = int(config['SERVER']['PORT'])

server.initialize()
server.app.run(debug=True,port=PORT)
