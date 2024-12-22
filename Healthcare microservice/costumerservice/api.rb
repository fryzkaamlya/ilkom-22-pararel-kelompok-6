require 'json'
require 'sinatra'
module CostumerService
    class API < Sinatra::Base
      get '/' do
        'ini'
      end
      get '/order/user/:user_id' do
        "List of orders for user #{params[:user_id]}"
      end
    end
end
