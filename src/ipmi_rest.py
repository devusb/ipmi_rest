import pyipmi
import pyipmi.interfaces
import json
from flask import Flask,jsonify,request



app = Flask(__name__)
@app.route('/status')
def status():
    hostname = request.args.get("hostname")
    port = request.args.get("port",type=int)
    username = request.args.get("username")
    password = request.args.get("password")
    target = request.args.get("target")

    interface = pyipmi.interfaces.create_interface('rmcp')
    connection = pyipmi.create_connection(interface)
    connection.target = pyipmi.Target(int(target,16))
    connection.session.set_session_type_rmcp(hostname, port=port)
    connection.session.set_auth_type_user(username, password)
    connection.session.establish()

    return jsonify({'power_state': connection.get_chassis_status().power_on})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port="5001",debug=True)

