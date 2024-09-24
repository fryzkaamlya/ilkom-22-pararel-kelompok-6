#app.rb
require 'sinatra'
require 'json'

module ItemService
    class API < Sinatra::Base
        #Simulasi database
        datamahasiswa = [
            {id: 1, name: "Bayyinahtun", nim: "F1G122001"},
            {id: 2, name: "Kumala", nim: "F1G122005"},
        ]

        get '/' do
            content_type :json
            'Hallo'.to_json 
        
        end

            get '/posts'do
            content_type :json
            datamahasiswa.to_json
        end
        
        get'/posts/:id' do
            content_type :json
            {'id'=> '1000'}.to_json
        end
    end
end

ItemService::API.run!