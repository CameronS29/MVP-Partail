class HomeController < ApplicationController
    before_action :authenticate_user!
    def index
        @publications = [
            "in vivo genome editing",
            "CAR T",
            "AAV AND immunogenicity",
            "aging",
            "cystic fibrosis therapies",
            "cardiac AND gene therapy",
            "regulatory t cell AND therapy",
            "Sickle cell AND CRISPR",
            "Triple negative breast cancer AND therapy",
            "Checkpoint inhibitor and resistance",
            "Covid-19 OR SARS-CoV-2",
            "Exosome",
            "Nanoparticle delivery OR non-viral delivery",
            "Bacteriophage",
            "Cell engineering",
            "Synthetic notch",
            "Gamma delta T cell",
            "mTOR",
            "klotho",
            "sarcopenia",
            "osteoarthritis",
            "inflammasome",
            "interstitial lung"
        ]
        @companies = [
            "Editas Medicine",
            "Intellia Therapeutics",
            "CRISPR Therapeutics",
            "Beam Therapeutics",
            "Bluebird Bio",
            "uniQure NV",
            "Sarepta Therapeutics",
            "RegenxBio",
            "MeiraGTx",
            "Orchard Therapeutics",
            "Axovant Gene Therapies",
            "Passage Bio",
            "Rocket Pharmaceuticals",
            "Decibel Therapeutics",
            "Sana Biotechnology",
            "Century Therapeutics",
            "Allogene Therapeutics",
            "Unity Biotechnology",
            "Navitor Pharmaceuticals",
            "resTOR Bio",
            "Arsenal Bio",
            "Sonoma Biosciences"
        ]
        @selected_publications = UserTopic.where("user_id = ? AND topic_type = 1", current_user.id)
        @selected_companies = UserTopic.where("user_id = ? AND topic_type = 2", current_user.id)
    end
    
    def deselect_topic
        topic = request.params[:id]
        UserTopic.where("user_id = ? AND topic = ?", current_user.id, topic).delete_all
        redirect_to({action: "index"})
    end

    def select_topic
        topic = request.params[:id]
        topic_type = request.params[:topic_type]
        user_topic = UserTopic.new(user_id: current_user.id, topic: topic, topic_type: topic_type)
        user_topic.save
        redirect_to({action: "index"})
    end

    def authenticate_user!
        if user_signed_in?
            super
        else
            redirect_to "/users/login", :notice => 'if you want to add a notice'
        ## if you want render 404 page
        ## render :file => File.join(Rails.root, 'public/404'), :formats => [:html], :status => 404, :layout => false
        end
    end
end
