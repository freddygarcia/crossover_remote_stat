from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def hello():
	dir(request)
	return "Hello World!"

app.run(debug=True)
