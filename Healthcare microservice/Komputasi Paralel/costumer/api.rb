require 'json'
require 'sinatra'
module CustomerService
  class API < Sinatra::Base
    get '/customers/:id' do
      id = params['id']
      content_type :json
     { id: id, name: 'rian'}.to_json
    end
   end
end
