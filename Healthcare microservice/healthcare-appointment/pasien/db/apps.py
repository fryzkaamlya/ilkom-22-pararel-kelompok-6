from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Konfigurasi database
db_config = 'C:/Users/my_hp/microservice.db'  # Ganti dengan nama file database SQLite Anda

@app.route('/pasien', methods=['GET'])  # Endpoint yang mendukung metode GET
def get_pasien():
    conn = None
    try:
        conn = sqlite3.connect(db_config)
        cursor = conn.cursor()

        sql = 'SELECT * FROM pasien'
        cursor.execute(sql)
        result = cursor.fetchall()

        # Mengonversi hasil menjadi dictionary
        columns = [column[0] for column in cursor.description]
        result_dict = [dict(zip(columns, row)) for row in result]

        return jsonify(result_dict)

    except sqlite3.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# POST request untuk menambahkan data
@app.route('/pasien', methods=['POST'])
def add_pasien():
    data = request.json
    conn = sqlite3.connect(db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pasien (nama_pasien, nik, no_hp) VALUES (?, ?, ?)",
        (data['nama_pasien'], data['nik'], data['no_hp']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'pasien added successfully'}), 201

# PUT request untuk memperbarui data
@app.route('/pasien/<int:id_pasien>', methods=['PUT'])
def update_pasien(id_pasien):
    data = request.get_json()
    nama_pasien = data.get("nama_pasien")
    nik = data.get("nik")
    no_hp = data.get("no_hp")

    try:
        conn = sqlite3.connect(db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE pasien SET nama_pasien = ?, nik = ?, no_hp = ? WHERE id_pasien = ?", (nama_pasien, nik, no_hp, id_pasien))
        conn.commit()
        return jsonify({"message": "Data pasien berhasil diperbarui"}), 200
    except sqlite3.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3333)