import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=' 192.168.1.37',  # Alamat IP server MySQL
            user='username',          # User MySQL
            password='kmpts_6!@#$',  # Password MySQL
            database='db_healthcare'  # Nama database
        )
        print("Koneksi ke database berhasil.")
        return connection
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan koneksi: {err}")
        raise