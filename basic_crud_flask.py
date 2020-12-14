from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config['DEBUG'] = True

pool = psycopg2.connect(database = "data_science", user = "upal", password = "240919",
host = "localhost", port = "5432", cursor_factory = RealDictCursor)
cur = pool.cursor()

@app.route('/addBus', methods = ['POST'])
def add_bus():
	bus = request.get_json()
	try:
		cur.execute("INSERT INTO bus_data (slno, number_plate, manufacturer, model, year, capacity) \
		VALUES ((SELECT coalesce(max(slno) + 1, 1) FROM bus_data), %s, %s, %s, %s, %s) RETURNING slno", \
		(bus.get('Number_Plate'), bus.get('Manufacturer'), bus.get('Model'), bus.get('Year'), bus.get('Capacity')))
		pool.commit()
		rows = cur.fetchall()
		if len(rows) == 0:
			return {'Status' : False, 'Message': 'Unable to Save Details..!!', 'Data': []}, 406
		else:
			return {'Status' : True, 'Message': 'Data Saved..!!', 'Data':[]}, 201
	except Exception as e:
		return {'Status' : False, 'Message': 'Internal Server Error..!!', 'Data':[]}, 500

@app.route('/getAllBus', methods = ['GET'])
def get_all_bus():
	try:
		cur.execute("SELECT number_plate, manufacturer, model, year, capacity FROM bus_data")
		rows = cur.fetchall()
		if len(rows) == 0:
			return {'Status' : False, 'Message': 'No Data Found..!!', 'Data': rows}, 404
		else:
			return {'Status' : True, 'Message': 'Data Found..!!', 'Data': rows}, 200
	except Exception as e:
		return {'Status' : False, 'Message': 'Internal Server Error..!!', 'Data':[]}, 500

@app.route('/getBus/<string:number_plate>', methods = ['GET'])
def get_bus(number_plate):
	try:
		cur.execute("SELECT number_plate, manufacturer, model, year, capacity FROM bus_data WHERE number_plate = %s", (number_plate,))
		rows = cur.fetchall()
		if len(rows) == 0:
			return {'Status' : False, 'Message': 'No Data Found..!!', 'Data': rows}, 404
		else:
			return {'Status' : True, 'Message': 'Data Found..!!', 'Data': rows}, 200
	except Exception as e:
		print(e)
		return {'Status' : False, 'Message': 'Internal Server Error..!!', 'Data':[]}, 500

@app.route('/updateSeatCapacity', methods = ['PUT'])
def update_capacity():
	bus = request.get_json()
	try:
		cur.execute("UPDATE bus_data SET capacity = %s WHERE number_plate = %s RETURNING capacity", (bus.get('Capacity'), bus.get('Number_Plate'),))
		pool.commit()
		rows = cur.fetchall()
		if len(rows) == 0:
			return {'Status' : False, 'Message': 'Failed to Update..!!', 'Data': []}, 406
		else:
			return {'Status' : True, 'Message': 'Data Updated..!!', 'Data': []}, 200
	except Exception as e:
		print(e)
		return {'Status' : False, 'Message': 'Internal Server Error..!!', 'Data':[]}, 500

@app.route('/deleteBus/<string:number_plate>', methods = ['DELETE'])
def delete_bus(number_plate):
	try:
		cur.execute("DELETE FROM bus_data WHERE number_plate = %s", (number_plate, ))
		pool.commit()
		return {'Status' : True, 'Message': 'Selected Bus Deleted..!!', 'Data': []}, 200
	except Exception as e:
		print(e)
		return {'Status' : False, 'Message': 'Internal Server Error..!!', 'Data':[]}, 500

app.run(port = 3000)