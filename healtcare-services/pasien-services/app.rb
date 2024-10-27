# app.rb
require 'sinatra'
require 'json'
require 'sequel'
require 'sqlite3'

# Koneksi ke database SQLite
DB = Sequel.connect(adapter: 'sqlite', database: 'D:/MITA FILE/Semester 5/Komputasi Paralel/microservices-learning/healtcare-services/pasien-services/db/patients.db')


# Buat tabel pasien jika belum ada
DB.create_table? :patients do
  primary_key :id
  String :name
  String :age
  String :contact_info
end

class Patient < Sequel::Model(:patients)
  def to_hash
    {
      id: id,
      name: name,
      age: age,
      contact_info: contact_info
    }
  end
end

# Cek koneksi
begin
  DB.test_connection
  puts "Koneksi ke database berhasil!"
rescue Sequel::DatabaseError => e
  puts "Koneksi ke database gagal: #{e.message}"
end

get '/' do
  'Hello World!'
end

# Get all patients
get '/patients' do
  content_type :json
  Patient.all.map(&:to_hash).to_json
end

# Add a new patient
post '/patients' do
  content_type :json
  new_patient = Patient.create(
    name: params[:name],
    age: params[:age],
    contact_info: params[:contact_info]
  )
  new_patient.to_hash.to_json  # Kembalikan data pasien yang baru ditambahkan
end

# Get a patient by ID
get '/patients/:id' do
  content_type :json
  patient = Patient[params[:id].to_i]
  if patient
    patient.to_hash.to_json
  else
    status 404
    { error: 'Patient not found' }.to_json
  end
end
