import pyipmi
import pyipmi.interfaces
from flask import Flask,jsonify,request


def create_ipmi(hostname,port,username,password,target):
    interface = pyipmi.interfaces.create_interface('rmcp')
    connection = pyipmi.create_connection(interface)
    connection.target = pyipmi.Target(int(target,16))
    connection.session.set_session_type_rmcp(hostname, port=port)
    connection.session.set_auth_type_user(username, password)
    connection.session.establish()
    return connection

app = Flask(__name__)
@app.route('/status')
def status():
    hostname = request.args.get("hostname")
    port = request.args.get("port",type=int)
    username = request.args.get("username")
    password = request.args.get("password")
    target = request.args.get("target")

    connection = create_ipmi(hostname,port,username,password,target)

    power_state = connection.get_chassis_status().power_on
    connection.session.close()

    return jsonify({'power_state': power_state})

@app.route('/power_on')
def power_on():
    hostname = request.args.get("hostname")
    port = request.args.get("port",type=int)
    username = request.args.get("username")
    password = request.args.get("password")
    target = request.args.get("target")

    connection = create_ipmi(hostname,port,username,password,target)

    connection.chassis_control_power_up()
    connection.session.close()

    return jsonify({'response': "power_on"})

@app.route('/power_off')
def power_off():
    hostname = request.args.get("hostname")
    port = request.args.get("port",type=int)
    username = request.args.get("username")
    password = request.args.get("password")
    target = request.args.get("target")

    connection = create_ipmi(hostname,port,username,password,target)

    connection.chassis_control_soft_shutdown()
    connection.session.close()

    return jsonify({'response': "power_off"})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port="5001",debug=True)

