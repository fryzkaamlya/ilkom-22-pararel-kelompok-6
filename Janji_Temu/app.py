import requests
from flask import Flask, request, jsonify
from crud import get_appointment_details, create_appointment, update_appointment, delete_appointment

app = Flask(__name__)


#request untuk servis dokter
def get_doctor_info(doctor_id):
    doctor_service_url = f'http://127.0.0.1:9000/doctors/{doctor_id}'
    response = requests.get(doctor_service_url)
    
    if response.status_code == 200:
        return response.json(), 200
    else:
        return {'message': 'Dokter tidak ditemukan'}, 404
    
#request untuk servis pasien  
def get_pasien_info(pasien_id):
    pasien_service_url = f'http://127.0.0.1:1212/pasien/{pasien_id}'
    response = requests.get(pasien_service_url)
    
    if response.status_code == 200:
        return response.json(), 200
    else:
        return {'message': 'Pasien tidak ditemukan'}, 404


@app.route('/janjitemu', methods=['GET'])
def get_appointments():
    return get_appointment_details()

@app.route('/janji-temu/<int:id_janji_temui>', methods=['GET'])
def get_appointment(id_janji_temui):
    # Mendapatkan informasi janji temu berdasarkan id
    janji_temui, status_code = get_appointment_details(id_janji_temui)
    if status_code != 200:
        return jsonify(janji_temui), status_code

    # Mendapatkan informasi dokter
    doctor_info, doctor_status_code = get_doctor_info(janji_temui['id_dokter'])
    if doctor_status_code != 200:
        return jsonify(doctor_info), doctor_status_code

    # Mendapatkan informasi pasien
    pasien_info, pasien_status_code = get_pasien_info(janji_temui['id_pasien'])
    if pasien_status_code != 200:
        return jsonify(pasien_info), pasien_status_code

    # Menyusun hasil dan mengembalikan informasi gabungan
    janji_temui['dokter'] = doctor_info
    janji_temui['pasien'] = pasien_info

    return jsonify(janji_temui), 200

@app.route('/janjitemu', methods=['POST'])
def add_appointment():
    data = request.json
    return create_appointment(data)

@app.route('/janjitemu/<int:id>', methods=['PUT'])
def modify_appointment(id):
    data = request.json
    return update_appointment(id, data)

@app.route('/janjitemu/<int:id>', methods=['DELETE'])
def remove_appointment(id):
    return delete_appointment(id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

