# app.py
import requests
from flask import Flask, request, jsonify
from crud import get_medical_records, create_medical_record, update_medical_record, delete_medical_record

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


@app.route('/rekam-medis', methods=['GET'])
def get_records():
    result, status_code = get_medical_records()
    return jsonify(result), status_code

@app.route('/rekam-medis', methods=['POST'])
def create_record():
    data = request.json
    result, status_code = create_medical_record(data)
    return jsonify(result), status_code

@app.route('/rekam-medis/<int:id_rekam_medis>', methods=['PUT'])
def update_record(id_rekam_medis):
    data = request.json
    result, status_code = update_medical_record(id_rekam_medis, data)
    return jsonify(result), status_code

@app.route('/rekam-medis/<int:id_rekam_medis>', methods=['DELETE'])
def delete_record(id_rekam_medis):
    result, status_code = delete_medical_record(id_rekam_medis)
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5678)
