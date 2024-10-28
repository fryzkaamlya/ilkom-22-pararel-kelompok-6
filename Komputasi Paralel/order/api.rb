require 'sinatra'
module OrderService
    class API < Sinatra::Base
        get '/' do
        'hi'
    end
        get '/order/user/:user_id' do
            "List of orders for user #{params[:user_id]}"
        end
        run! if app_file == $0
    end
end

not_found do
    'This page does not exist.'
  end