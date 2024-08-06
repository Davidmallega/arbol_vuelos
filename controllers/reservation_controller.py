from flask import Blueprint, render_template, request, redirect, url_for
from models.reservation import FlightReservationSystem

control_de_reservas = Blueprint('control_de_reservas', __name__)

sistema_de_vuelos = FlightReservationSystem()

@control_de_reservas.route('/')
def index():
    return redirect(url_for('control_de_reservas.vuelos_disponibles'))

@control_de_reservas.route('/vuelos_disponibles')
def vuelos_disponibles():
    vuelos = sistema_de_vuelos.get_vuelos_disponibles()
    return render_template('flight_list.html', vuelos=vuelos)

@control_de_reservas.route('/reservations')
def reservations():
    reservations = sistema_de_vuelos.inorder_traversal(sistema_de_vuelos.root)
    return render_template('reservation_list.html', reservations=reservations)

@control_de_reservas.route('/delete/<int:vuelo_id>', methods=['POST'])
def delete_reservation(vuelo_id):
    sistema_de_vuelos.delete(vuelo_id)
    return redirect(url_for('control_de_reservas.reservations'))

@control_de_reservas.route('/seleccionar_asientos/<int:vuelo_id>', methods=['POST'])
def seleccionar_asientos(vuelo_id):
    nombre_pasajero = request.form['nombre_pasajero']
    return render_template('seleccionar_asientos.html', vuelo_id=vuelo_id, nombre_pasajero=nombre_pasajero)

@control_de_reservas.route('/reservar_vuelo/<int:vuelo_id>', methods=['POST'])
def reservar_vuelo(vuelo_id):
    vuelo = next((vuelo for vuelo in sistema_de_vuelos.get_vuelos_disponibles() if vuelo['vuelo_id'] == vuelo_id), None)
    if vuelo:
        nombre_pasajero = request.form['nombre_pasajero']
        asientos = request.form['asientos']
        sistema_de_vuelos.insert(vuelo_id, nombre_pasajero, vuelo['fecha'], vuelo['pais_origen'], vuelo['pais_destino'], asientos)
    return redirect(url_for('control_de_reservas.reservations'))


