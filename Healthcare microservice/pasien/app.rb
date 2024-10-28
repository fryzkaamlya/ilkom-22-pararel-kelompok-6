from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Konfigurasi database
db_config = {
    'user': 'root',
    'password': '',  # Ganti dengan password Anda jika ada
    'host': '127.0.0.1',
    'database': 'healthcare_microservice'
}

@app.route('/pasien', methods=['GET'])  # Endpoint yang mendukung metode GET
def get_pasien():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        sql = 'SELECT * FROM pasien'
        cursor.execute(sql)
        result = cursor.fetchall()

        return jsonify(result)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()

if _name_ == '_main_':
    app.run(debug=True, host='0.0.0.0', port=5111)