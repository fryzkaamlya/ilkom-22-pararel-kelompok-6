require 'sinatra'
require 'sequel'
require 'json'

# Koneksi ke database SQLite
begin
  DB = Sequel.connect('sqlite:///C:/Users/ASUS_/OneDrive/Documents/Janji%20Temu/DB_janji_temu.db')
  puts "Koneksi ke database berhasil!"
rescue Sequel::DatabaseConnectionError => e
  puts "Error connecting to the database: #{e.message}"
  exit
end

# Referensi ke tabel janji_temu, dokter, dan pasien
Janji_Temu = DB[:janji_temu]
Dokter = DB[:dokter]
Pasien = DB[:pasien]

# Tes server
get '/' do
  'Hello, World!'
end

# Endpoint untuk mendapatkan semua janji temu
get '/Janji_Temu' do
  appointments = Janji_Temu.all
  content_type :json
  appointments.to_json
end

# Endpoint untuk membuat janji temu baru dengan foreign key dokter_id dan pasien_id
post '/Janji_Temu' do
  begin
    data = JSON.parse(request.body.read)
  rescue JSON::ParserError
    status 400
    return { message: 'Input JSON tidak valid' }.to_json
  end

  # Cek apakah dokter dengan Id_Dokter yang diberikan ada
  Id_Dokter = data['Id_Dokter']
  unless Dokter.where(id: Id_Dokter).first
    status 400
    return { message: 'Dokter tidak valid atau tidak ditemukan' }.to_json
  end

  # Cek apakah pasien dengan Id_Pasien yang diberikan ada
  Id_Pasien = data['Id_Pasien']
  unless Pasien.where(id: Id_Pasien).first
    status 400
    return { message: 'Pasien tidak valid atau tidak ditemukan' }.to_json
  end
  
  # Buat janji temu baru dengan informasi yang valid
  new_Janjitemu = {
    Id_Dokter: Id_Dokter,
    Id_Pasien: Id_Pasien,
    Tanggal: data['Tanggal'],
    Tujuan: data['Tujuan']
  }
  
  Janji_Temu.insert(new_Janjitemu)
  status 201
  { message: 'Janji temu berhasil dibuat' }.to_json
end

# Endpoint untuk mendapatkan janji temu berdasarkan ID
get '/Janji_Temu/:id' do
  id = params['id'].to_i
  appointment = Janji_Temu.where(id: id).first
  
  if appointment
    content_type :json
    appointment.to_json
  else
    status 404
    { message: 'Janji temu tidak ditemukan' }.to_json
  end
end
