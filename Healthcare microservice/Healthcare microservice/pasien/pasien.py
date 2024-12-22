from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Konfigurasi koneksi ke database MySQL
config = {
    'user': 'root',           # Sesuaikan dengan username MySQL Anda
    'password': '',           # Isi password MySQL, atau kosong jika tidak ada
    'host': '127.0.0.1',
    'database': 'healthcare microservice'    # Nama database yang telah dibuat di MySQL
}

# Fungsi untuk membuat koneksi ke database
def get_db_connection():
    conn = mysql.connector.connect(**config)
    return conn

# Route untuk mendapatkan semua data user
@app.route('/pasien', methods=['GET'])
def get_pasien():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pasien")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(pasien)

# Route untuk menambah user baru
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "User berhasil ditambahkan"}), 201

# Route untuk memperbarui user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "User berhasil diperbarui"})

# Route untuk menghapus user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "User berhasil dihapus"})

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True)