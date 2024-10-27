# app.rb
require 'sinatra'
require 'json'

appointments = [
    {id: 1, patient_id: 2, doctor_id: 1, appointment_time: "2024-09-30 14:00"}
]

#tes server
get '/' do
    'Hello world!'
end

# Get all appointments
get '/appointments' do
  content_type :json
  appointments.to_json
end

# Create a new appointment
post '/appointments' do
  content_type :json
  # Get patient and doctor info by ID
  patient_id = params[:patient_id]
  doctor_id = params[:doctor_id]

  patient = get_service_data("http://localhost:8080/patients/#{patient_id}")
  doctor = get_service_data("http://localhost:8989/doctors/#{doctor_id}")

  if patient && doctor
    new_appointment = {
      id: appointments.size + 1,
      patient: patient,
      doctor: doctor,
      appointment_time: params[:appointment_time]
    }
    appointments << new_appointment
    new_appointment.to_json
  else
    status 404
    { error: 'Patient or Doctor not found' }.to_json
  end
end

# Helper function to get data from other services
def get_service_data(url)
  uri = URI(url)
  response = Net::HTTP.get(uri)
  JSON.parse(response) rescue nil
end
