from time import time
from pony.orm import *
from flask import *
from decimal import Decimal
from datetime import datetime, date

db = Database()

def func():
    db.bind(provider='mysql', host='127.0.0.1', port=3306, user='root', passwd='root', db='hotelace')
    db.generate_mapping(create_tables=True)
    set_sql_debug(True)

class Hotel(db.Entity):
    id = PrimaryKey(int, auto=True)
    hotel_name = Required(str, 50) 
    email = Required(str, 50)
    phone_number = Required(str, 10)
    address = Required(str, 40)
    postcode = Required(int)
    city = Required(str, 80)
    country = Required(str, 60)

class Room(db.Entity):
    id = PrimaryKey(int, auto = True)
    id_hotel_room = Required(int)
    room_type = Required(str, 10, py_check=lambda room_type: room_type == 'Single' or room_type == 'Double' or room_type == 'Deluxe')
    room_status = Required(str, py_check=lambda room_status: room_status == 'Occupied' or room_status == 'Unoccupied')
    price = Required(Decimal)
  
@db_session()
def get_hotel_occupancy():
    #occupied_rooms = count(r for r in Room if r.room_status == 'Occupied')
    #unoccupied_rooms = count(r for r in Room if r.room_status== 'Unoccupied' or r.room_status == 'Occupied')
    #result = ((occupied_rooms/unoccupied_rooms)*100)
    #return result
    db_querry = select(x for x in Room)[:]
    result = []
    for r in db_querry:
        result.append(r.to_dict())
    return result

class Customer(db.Entity):
    id = PrimaryKey(int, auto=True)
    customer_name = Required(str, 40)
    surname = Required(str, 40)
    email = Required(str, 50)
    phone_number = Required(str,15,unique=True)
    address = Required(str, 40)
    postcode =Required(int)
    city = Required(str, 80)
    country = Required(str, 60)

@db_session()
def add_guest(json_request):
    try:
        customer_name = json_request['customer_name']
        surname = json_request['surname']
        email = json_request['email']
        phone_number = json_request['phone_number']
        address = json_request['address']
        postcode = json_request['postcode']
        city = json_request['city']
        country = json_request['country']  
        print(json_request)
        Customer(customer_name = customer_name, surname = surname, email = email, phone_number = phone_number, address = address, postcode = postcode, city = city, country = country)
        response = {
            "status" : "Success"
        }
        return response
    except Exception as e:
        response = {
            "status" : "Fail",
            "error" : str(e)
        }
        return response

@db_session
def get_guest(id):
    customer = Customer.get(id=id)
    return customer.to_dict()

@db_session
def update_guest(id, data):
    try:
        customer = Customer.get_for_update(id=id)
        customer.customer_name = data.get('customer_name') 
        customer.surname = data.get('surname')
        customer.email = data.get('email')
        customer.phone_number = data.get('phone_number')
        customer.address = data.get('address')
        customer.postcode = data.get('postcode')
        customer.city = data.get('city')
        customer.country = data.get('country')
    except:
        return "Guest has been unsuccessfully updated"
    else:
        return "Guest has been successfully updated"

@db_session()
def delete_guest(id):
    try:
        Customer[id].delete()
    except:
        return "Guest has been unsuccessfully deleted"
    else:
        return "Guest has been successfully deleted"
        

@db_session
def get_guest_info():
    try:
        customer_list = select(x for x in Customer)[:]
        result = []
        for item in customer_list :
            result.append(item.to_dict())
        response = {
            "status" : "Success",
            "data": result
        }
        return response
    except Exception as e:
        response = {
            "status": "Fail", 
            "error": str(e)
        }
        return response

@db_session()
def update_info():
    try:
        customer_info = select(c for c in Customer)[:]
        result = []
        for item in customer_info :
            result.append(item.to_dict())
        response = {
            "status" : "Success",
            "data": result
        }
        return response
    except Exception as e:
        response = {
            "status": "Fail", 
            "error": str(e)
        }
        return response

class Booking(db.Entity):
    id = PrimaryKey(int, auto=True)
    id_room = Optional(int, auto=True)
    id_customer = Optional(int, auto =True)
    booking_status = Required(str, 20, py_check=lambda booking_status: booking_status == 'PENDING' or booking_status == 'CONFIRMED' or booking_status == 'CANCELLED')
    start_time = Required(date)
    end_time = Required(date)
    requirement = Required(str, 20, py_check=lambda Requirement: Requirement == 'No Preference' or Requirement == 'Non Smoking' or Requirement == 'Smoking')
    adults = Required(int)
    children = Required(int)
    parking_space = Required(str, 5, py_check=lambda parkingSpace: parkingSpace == 'Yes' or parkingSpace == 'No')
    breakfast_included = Required(str, 5, py_check=lambda breakfast: breakfast == 'Yes' or breakfast == 'No')
    swimming_pool = Required(str, 5, py_check=lambda swimmingPool: swimmingPool == 'Yes' or swimmingPool == 'No')
    wellness_spa = Required(str, 5, py_check=lambda wellnessSpa : wellnessSpa == 'Yes' or wellnessSpa == 'No')
    requests = Optional(str, 500)
    time_stamp = Optional(datetime)

@db_session()
def get_guest_reservation():
    try:
        booking_list = select(x for x in Booking)[:]
        result = []
        for item in booking_list :
            result.append(item.to_dict())
        response = {
            "status" : "Success",
            "data": result
        }
        return response
    except Exception as e:
        response = {
            "status": "Fail", 
            "error": str(e)
        }
        return response

@db_session()
def add_guest_booking(json_request):
    try:
        start_time = json_request['start_time']
        end_time = json_request['end_time']
        adults = json_request['adults']
        children = json_request['children']
        parking_space = json_request['parking_space']
        breakfast_included = json_request['breakfast_included']
        swimming_pool = json_request['swimming_pool']
        wellness_spa = json_request['wellness_spa']
        requirement = json_request['requirement']  
        requests = json_request['requests']
        booking_status = json_request['booking_status'].upper()
        print(json_request) 
        Booking(start_time = start_time, end_time = end_time, adults = adults, children = children, parking_space = parking_space, breakfast_included = breakfast_included,
        swimming_pool = swimming_pool, wellness_spa = wellness_spa, requirement = requirement, booking_status = booking_status, requests = requests)
        response = {
            "status":"Success"
        }
        return response
    except Exception as e:
        response = { 
            "status" : "Fail",
            "error" : str(e)
        }
        return response

class Bill(db.Entity):
    id = PrimaryKey(int,auto=True)
    id_booking = Required(int)
    room_charge = Required(int) 
    bar_charge = Required(int)
    restauraunt_charge = Required(int)
    total_price = Required(int)
    payment_date = Required(datetime) 

class Employee(db.Entity):
    id = PrimaryKey(int, auto=True)
    id_hotel = Required(int)
    employee_name = Required(str, 40)
    surname = Required(str, 40)
    email = Required(str, 50)
    phone_number = Required(str, unique=True)


