from flask import *
from flask import Flask
import db_connector
from db_connector import *


app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/guest/', methods=['GET'])
def guest():
    return render_template("guest.html")

@app.route('/employee/', methods=['GET'])
def employee():
    return render_template("employee.html")

@app.route('/guest/info/', methods=['GET','POST'])
def guest_information():
    if request.method == 'POST':
        try:
            json_request = {}
            print(json_request)
            for key, value in request.form.items(): #proalzimo krozdictionary za key i values
                json_request[key]=value
        except Exception as e:
            response = {"status": str(e)}
            return make_response(jsonify(response), 400)
        response = db_connector.add_guest(json_request)
        if response["status"] == "Success":
            return make_response(render_template("guest_information.html"), 200)
        else: 
            return make_response(jsonify(response), 400)
    else: 
        return render_template("guest_information.html")

@app.route('/guest/booking', methods=['GET','POST'])
def guest_booking():
    if request.method == 'POST':
        try:
            json_request = {}
            print(json_request)
            for key, value in request.form.items():
                json_request[key]=value
            response = db_connector.add_guest_booking(json_request)
        except Exception as e:
            response = {"status": str(e)}
            return make_response(jsonify(response), 400)
        else:
            if response["status"] == "Success":
                return make_response(render_template("create_booking.html"), 200)
            else: 
                return make_response(jsonify(response), 400)
    else:
        return render_template("guest_booking.html")

#employee creates booking
@app.route('/employee/booking', methods=['GET','POST'])
def create_booking():
    if request.method== 'POST':
        try:
            json_request = {}
            for key, value in request.form.items():
                json_request[key]=value
            response = db_connector.add_guest_booking(json_request)
        except Exception as e:
            response = {"status": str(e)}
            return make_response(jsonify(response), 400)
        if response["status"] == "Success":
            return make_response(render_template("create_booking.html"), 200)
        else: 
            return make_response(jsonify(response), 400)
    else:
        return render_template("create_booking.html")

#emmployee creates guest's information
@app.route('/employee/info', methods=['GET','POST'])
def create_information():
    if request.method== 'POST':
        try:
            json_request = {}
            print(json_request)
            for key, value in request.form.items(): #proalzimo krozdictionary za key i values
                json_request[key]=value
        except Exception as e:
            response = {"status": str(e)}
            return make_response(jsonify(response), 400)
        response = db_connector.add_guest(json_request)
        if response["status"] == "Success":
            return make_response(render_template("create_information.html"), 200)
        else: 
            return make_response(jsonify(response), 400)
    else: 
        return render_template("create_information.html")

#employee reads info
@app.route('/employee/info/', methods=['GET'])
def read_information():
    response = db_connector.get_guest_info()
    if response["status"] == "Success":
        return make_response(render_template("read_information.html", info = response["data"]), 200)
    else:
        return make_response(jsonify(response["error"]), 400)

#employee reads booking
@app.route('/employee/booking/', methods=['GET'])
def read_booking():
    response = db_connector.get_guest_reservation()
    if response["status"] == "Success":
        return make_response(render_template("read_booking.html", information = response["data"]), 200)
    else:
        return make_response(jsonify(response["error"]), 400)

#employee updates guest
@app.route('/employee/info/<id>', methods=['GET','POST']) #POST is actually UPDATE
def update_information(id):
    if request.method == 'GET':
        response = db_connector.get_guest(id)
        return make_response(render_template("update_information.html", guest=response), 200)
    else:
        response = db_connector.update_guest(id, request.form)
        return response

#employee deletes guest's info
@app.route('/employee/information/<id>', methods=['POST'])
def delete_information(id):
    if request.method == 'POST':
        response = db_connector.delete_guest(id)
        return response
    else:
        return make_response(405)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'website' 
    db_connector.func()
    app.run(host='127.0.0.1', port=9000)
