require 'sinatra'
require 'active_record'
require 'json'

# Koneksi ke database
ActiveRecord::Base.establish_connection(
  adapter: 'mysql2',
  host: 'localhost',
  username: 'root', # Ganti dengan username database Anda
  password: '',  # Ganti dengan password database Anda
  database: 'microservice'    # Ganti dengan nama database Anda
)

class Pasien < ActiveRecord::Base
  self.table_name = "pasien" # Ganti dengan nama tabel Anda
end

# Route untuk menampilkan halaman data pasien
get '/data_pasien' do
  erb :pasien # Menggunakan ERB untuk merender views/pasien.html
end

# Route untuk mengambil data pasien
get '/pasien' do
  pasien_data = Pasien.all
  pasien_data.to_json
end
