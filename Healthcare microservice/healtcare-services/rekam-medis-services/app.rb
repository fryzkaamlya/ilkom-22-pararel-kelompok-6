require 'sinatra'
require 'json'

#DB = Sequel.connect('sqlite://db/medical_records.db')

# Buat tabel rekam medis jika belum ada
#DB.create_table? :medical_records do
 #Integer :patient_id
  #Integer :doctor_id
  #String :diagnosis
  #String :treatment
  #String :visit_date
#end

#class MedicalRecord < Sequel::Model(:medical_records)
#end

medical_records= []

# Root Route
get '/' do
  'Rekam Medis Service is running!'
end

# Endpoint untuk mendapatkan semua rekam medis
get '/records' do
  content_type :json
  MedicalRecord.all.to_json
end

# Endpoint untuk menambahkan rekam medis baru
post '/records' do
  data = JSON.parse(request.body.read)
  record = MedicalRecord.create(
    patient_id: data['patient_id'],
    doctor_id: data['doctor_id'],
    diagnosis: data['diagnosis'],
    treatment: data['treatment'],
    visit_date: data['visit_date']
  )
  record.to_json
end
