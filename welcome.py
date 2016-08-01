import os
from flask import Flask, request, jsonify
import server.processImage

app = Flask(__name__)

app.static_folder = 'static'

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/frontDoc.html')
def FrontDoc():
    return app.send_static_file('frontDoc.html')

@app.route('/backDoc.html')
def BackDoc():
    return app.send_static_file('backDoc.html')

@app.route('/index.html')
def index():
    return app.send_static_file('index.html')
    
@app.route('/_passLink')
def passLink():
	try:
		return server.processImage.classify(request.args.get('input'))
	except Exception as e:
		try:
			return 'ERROR: ' + str(e)
		except:
			return 'ERROR: ???'

@app.errorhandler(404)
def notFound(err):
	return app.send_static_file('404.html')

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
