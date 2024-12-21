from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Fungsi untuk membuat koneksi ke database MySQL
def get_db_connection():
    return pymysql.connect(
        host='192.168.28.32',  # Ganti dengan IP atau alamat host MySQL
        user='username',      # Ganti dengan username MySQL
        password='kmpts_6!@#$', # Ganti dengan password MySQL
        database='db_healthcare',
        port=3306             # Port default MySQL
    )

# Fungsi untuk membuat tabel pasien jika belum ada
def create_pasien_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pasien (
            id_pasien INT AUTO_INCREMENT PRIMARY KEY,
            nama_pasien VARCHAR(50) NOT NULL,
            alamat VARCHAR(30) NOT NULL,
            jenis_kelamin VARCHAR(20) NOT NULL,
            diagnosa VARCHAR(50) NOT NULL
        )
    """)

    cursor.close()
    conn.close()

# Panggil fungsi untuk membuat tabel saat aplikasi dijalankan
create_pasien_table()

# Endpoint untuk mengambil data pasien (GET)
@app.route('/pasien', methods=['GET'])
def get_pasien():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tb_pasien")
    pasien_list = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    result_dict = [dict(zip(columns, row)) for row in pasien_list]

    cursor.close()
    conn.close()

    return jsonify(result_dict)

# Endpoint untuk menambahkan data pasien (POST)
@app.route('/pasien', methods=['POST'])
def add_pasien():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tb_pasien (name_pasien, alamat, jenis_kelamin, diagnosa) VALUES (%s, %s, %s, %s)",
                (data['name_pasien'], data['alamat'], data['jenis_kelamin'], data['diagnosa']))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'Pasien berhasil ditambahkan'}), 201

# Endpoint untuk memperbarui data pasien (PUT)
@app.route('/pasien/<int:id_pasien>', methods=['PUT'])
def update_pasien(id_pasien):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tb_pasien 
        SET name_pasien = %s, alamat = %s, jenis_kelamin = %s,  diagnosa = %s
        WHERE id_pasien = %s
    """, (data['name_pasien'], data['alamat'], data['jenis_kelamin'], data['diagnosa'], id_pasien))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'Data pasien berhasil diperbarui'}), 200

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1212)
