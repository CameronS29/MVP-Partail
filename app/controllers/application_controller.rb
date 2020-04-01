class ApplicationController < ActionController::Base
   # before_action :authenticate_user
  
    protected
  
    def configure_permitted_parameters
      devise_parameter_sanitizer.permit(:sign_up, keys: [:username])
    end
    
    def authenticate_user
        if user_signed_in?
            super
        else
            redirect_to "/users/login", :notice => 'if you want to add a notice'
        ## if you want render 404 page
        ## render :file => File.join(Rails.root, 'public/404'), :formats => [:html], :status => 404, :layout => false
        end
    end
  end