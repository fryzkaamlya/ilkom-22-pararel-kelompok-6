from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Konfigurasi database
db_config = 'D:/Database.db' # Ganti dengan nama file database SQLite Anda

@app.route('/Dokter', methods=['GET'])  # Endpoint yang mendukung metode GET
def get_Dokter():
    conn = None
    try:
        conn = sqlite3.connect(db_config)
        cursor = conn.cursor()

        sql = 'SELECT * FROM Dokter'
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
@app.route('/Dokter', methods=['POST'])
def add_Dokter():
    data = request.json
    conn = sqlite3.connect(db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Dokter (Nama_Dokter, Spesialis) VALUES (?, ?)",
                   (data['Nama_Dokter'], data['Spesialis']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Dokter added successfully'}), 201

# PUT request untuk memperbarui data
@app.route('/Dokter/<int:Id_Dokter>', methods=['PUT'])
def update_Dokter(Id_Dokter ):
    data = request.get_json()
    Nama_Dokter = data.get("Nama_Dokter")
    Spesialis = data.get("Spesialis")

    try:
        conn = sqlite3.connect(db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE dokter SET Nama_Dokter = ?, Spesialis = ? WHERE Id_Dokter = ?", (Nama_Dokter, Spesialis, Id_Dokter))
        conn.commit()
        return jsonify({"message": "Data dokter berhasil diperbarui"}), 200
    except sqlite3.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1211)