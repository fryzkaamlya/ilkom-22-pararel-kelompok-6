from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Konfigurasi database
db_config = 'C:/Users/acer/Documents/Rekam medis/rekam_medis1.db'  # Sesuaikan path database SQLite Anda

# Fungsi untuk mendapatkan koneksi database
def get_db_connection():
    conn = sqlite3.connect(db_config)
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint GET untuk daftar dokter
@app.route('/dokter', methods=['GET'])
def get_dokter():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM Dokter')
    dokter = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(dokter)

# Endpoint POST untuk menambah dokter
@app.route('/dokter', methods=['POST'])
def add_dokter():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Dokter (nama, spesialisasi) VALUES (?, ?)",
                   (data['nama'], data['spesialisasi']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Dokter berhasil ditambahkan'}), 201

# Endpoint GET untuk daftar pasien
@app.route('/pasien', methods=['GET'])
def get_pasien():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM Pasien')
    pasien = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(pasien)

# Endpoint POST untuk menambah pasien
@app.route('/pasien', methods=['POST'])
def add_pasien():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Pasien (nama, nik, nohp) VALUES (?, ?, ?)",
                   (data['nama'], data['nik'], data['nohp']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Pasien berhasil ditambahkan'}), 201

# Endpoint GET untuk daftar janji temu
@app.route('/Janji_temu', methods=['GET'])
def get_janji_temu():
    conn = get_db_connection()
    cursor = conn.execute('''SELECT jt.*, d.nama AS nama_dokter, p.nama AS nama_pasien
                             FROM Janji_temu jt
                             JOIN Dokter d ON jt.id_dokter = d.id_dokter
                             JOIN Pasien p ON jt.id_pasien = p.id_pasien''')
    janji_temu = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Print janji_temu for debugging
    print(janji_temu)
    
    return jsonify(janji_temu)


# Endpoint POST untuk menambah janji temu
@app.route('/janji_temu', methods=['POST'])
def add_janji_temu():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Janji_temu (id_pasien, id_dokter, tanggal, waktu) VALUES (?, ?, ?, ?)",
                   (data['id_pasien'], data['id_dokter'], data['tanggal'], data['waktu']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Janji temu berhasil ditambahkan'}), 201

# Endpoint GET untuk rekam medis berdasarkan ID pasien
@app.route('/rekam_medis/<int:id_pasien>', methods=['GET'])
def get_rekam_medis(id_pasien):
    print(f"Memanggil get_rekam_medis dengan id_pasien: {id_pasien}")  # Log ID yang diterima
    conn = get_db_connection()
    cursor = conn.execute('''SELECT rm.*, d.nama AS nama_dokter, jt.tanggal AS tanggal_janji
                             FROM rekam_medis rm
                             JOIN Dokter d ON rm.id_dokter = d.id_dokter
                             JOIN Janji_temu jt ON rm.id_janji_temu = jt.id_janji_temu
                             WHERE rm.id_pasien = ?''', (id_pasien,))
    rekam_medis = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(rekam_medis)

# Endpoint POST untuk menambah rekam medis
@app.route('/rekam_medis', methods=['POST'])
def add_rekam_medis():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Rekam_medis (id_pasien, id_dokter, id_janji_temu, diagnosa, tanggal) VALUES (?, ?, ?, ?, ?)",
                       (data['id_pasien'], data['id_dokter'], data['id_janji_temu'], data['diagnosa'], data['tanggal']))
        conn.commit()
        return jsonify({'message': 'Rekam medis berhasil ditambahkan'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()


@app.route('/routes', methods=['GET'])
def show_routes():
    output = []
    for rule in app.url_map.iter_rules():
        output.append(f"{rule.endpoint}: {rule.rule}")
    return jsonify(output)

# Endpoint root untuk path /
@app.route('/')
def home():
    return "Selamat datang di layanan rekam medis!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2211)
