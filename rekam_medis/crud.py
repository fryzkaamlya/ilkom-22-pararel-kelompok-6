# crud.py
from db_config import get_db_connection
import mysql.connector
from datetime import datetime

def get_medical_records():
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT 
                mr.id_rekam_medis, 
                p.name_pasien AS nama_pasien, 
                d.nama_dokter AS nama_dokter, 
                mr.diagnosis, 
                mr.tanggal 
            FROM 
                rekam_medis mr
            JOIN 
                tb_pasien p ON mr.id_pasien = p.id_pasien
            JOIN 
                tb_doctor d ON mr.id_dokter = d.id_dokter
        """
        cursor.execute(query)
        records = cursor.fetchall()

        if not records:
            return {"status": "success", "message": "Tidak ada rekam medis ditemukan", "data": []}, 200

        return {"status": "success", "data": records}, 200

    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil data rekam medis: {e}")
        return {"status": "error", "message": str(e)}, 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def create_medical_record(data):
    connection = None
    cursor = None
    try:
        id_pasien = data.get('id_pasien')
        id_dokter = data.get('id_dokter')
        diagnosis = data.get('diagnosis')
        tanggal = data.get('tanggal')

        # Validasi input
        if not id_pasien or not id_dokter or not diagnosis or not tanggal:
            return {"status": "error", "message": "Semua data harus diisi!"}, 400

        # Validasi format tanggal
        try:
            datetime.strptime(tanggal, '%Y-%m-%d')
        except ValueError:
            return {"status": "error", "message": "Format tanggal harus YYYY-MM-DD"}, 400

        connection = get_db_connection()
        cursor = connection.cursor()

        # Periksa apakah id_pasien dan id_dokter valid
        cursor.execute("SELECT id_pasien FROM tb_pasien WHERE id_pasien = %s", (id_pasien,))
        if not cursor.fetchone():
            return {"status": "error", "message": "Pasien tidak ditemukan!"}, 404

        cursor.execute("SELECT id_dokter FROM tb_doctor WHERE id_dokter = %s", (id_dokter,))
        if not cursor.fetchone():
            return {"status": "error", "message": "Dokter tidak ditemukan!"}, 404

        # Menambahkan rekam medis baru
        query = """
            INSERT INTO rekam_medis (id_pasien, id_dokter, diagnosis, tanggal)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (id_pasien, id_dokter, diagnosis, tanggal))
        connection.commit()

        return {"status": "success", "message": "Rekam medis berhasil ditambahkan!"}, 201

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan saat menambahkan rekam medis: {err}")
        return {"status": "error", "message": f"Terjadi kesalahan database: {err}"}, 500

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return {"status": "error", "message": str(e)}, 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def update_medical_record(id_rekam_medis, data):
    connection = None
    cursor = None
    try:
        diagnosis = data.get('diagnosis')
        tanggal = data.get('tanggal')

        # Validasi input
        if not diagnosis or not tanggal:
            return {"status": "error", "message": "Diagnosis dan tanggal harus diisi!"}, 400

        # Validasi format tanggal
        try:
            datetime.strptime(tanggal, '%Y-%m-%d')
        except ValueError:
            return {"status": "error", "message": "Format tanggal harus YYYY-MM-DD"}, 400

        connection = get_db_connection()
        cursor = connection.cursor()

        # Periksa apakah rekam medis dengan ID tersebut ada
        cursor.execute("SELECT id_rekam_medis FROM rekam_medis WHERE id_rekam_medis = %s", (id_rekam_medis,))
        if not cursor.fetchone():
            return {"status": "error", "message": "Rekam medis tidak ditemukan!"}, 404

        # Update rekam medis
        query = """
            UPDATE rekam_medis 
            SET diagnosis = %s, tanggal = %s
            WHERE id_rekam_medis = %s
        """
        cursor.execute(query, (diagnosis, tanggal, id_rekam_medis))
        connection.commit()

        return {"status": "success", "message": "Rekam medis berhasil diperbarui!"}, 200

    except Exception as e:
        print(f"Terjadi kesalahan saat memperbarui rekam medis: {e}")
        return {"status": "error", "message": str(e)}, 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def delete_medical_record(id_rekam_medis):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Periksa apakah rekam medis dengan ID tersebut ada
        cursor.execute("SELECT id_rekam_medis FROM rekam_medis WHERE id_rekam_medis = %s", (id_rekam_medis,))
        if not cursor.fetchone():
            return {"status": "error", "message": "Rekam medis tidak ditemukan!"}, 404

        # Hapus rekam medis
        cursor.execute("DELETE FROM rekam_medis WHERE id_rekam_medis = %s", (id_rekam_medis,))
        connection.commit()

        return {"status": "success", "message": f"Rekam medis dengan ID {id_rekam_medis} berhasil dihapus!"}, 200

    except Exception as e:
        print(f"Terjadi kesalahan saat menghapus rekam medis: {e}")
        return {"status": "error", "message": str(e)}, 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
