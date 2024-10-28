require 'sinatra'
require 'json'
require 'sequel'

DB = Sequel.connect(adapter: 'sqlite', database: 'D:/MITA FILE/Semester 5/Komputasi Paralel/microservices-learning/healtcare-services/dokter-services/db/doctors.db')

# Buat tabel dokter jika belum ada
DB.create_table? :doctors do
  primary_key :id
  String :name
  String :specialty  # Spesialisasi
end

class Doctor < Sequel::Model(:doctors)
  def to_hash
    {
      id: id,
      name: name,
      specialty: specialty
    }
  end
end

# Root Route
get '/' do
  'Dokter Service is running!'
end

# Get all patients
get '/doctors' do
  content_type :json
  Doctor.all.map(&:to_hash).to_json
end

# Add a new patient
post '/doctors' do
  content_type :json
  new_doctors = Doctor.create(
    name: params[:name],
    specialty: params[:age]
  )
  new_doctors.to_hash.to_json  # Kembalikan data pasien yang baru ditambahkan
end

# Get a patient by ID
get '/doctors/:id' do
  content_type :json
  doctors = Doctor[params[:id].to_i]
  if doctors
    doctors.to_hash.to_json
  else
    status 404
    { error: 'Doctors not found' }.to_json
  end
end
