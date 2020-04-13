class HomeController < ApplicationController
    before_action :authenticate_user!
    def index
        @publications = [
            "\"in vivo genome editing\"",
            "\"CAR T\"",
            "\"AAV\" AND \"immunogenicity\"",
            "aging",
            "\"cystic fibrosis therapies\"",
            "\"cardiac\" AND \"gene therapy\"",
            "\"regulatory t cell\" AND \"therapy\"",
            "\"Sickle cell\" AND \"CRISPR\"",
            "\"Triple negative breast cancer\" AND \"therapy\"",
            "\"Checkpoint inhibitor and resistance\"",
            "\"Covid-19\" OR \"SARS-CoV-2\"",
            "\"Exosome\"",
            "\"Nanoparticle delivery\" OR \"non-viral delivery\"",
            "\"Bacteriophage\"",
            "\"Cell engineering\"",
            "\"Synthetic notch\"",
            "\"Gamma delta T cell\"",
            "\"mTOR\"",
            "\"klotho\"",
            "\"sarcopenia\"",
            "\"osteoarthritis\"",
            "\"inflammasome\"",
            "\"interstitial lung\"",
            "\"ovarian cancer\""
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
            "Sonoma Biosciences",
            "Harpoon Therapeutics",
            "Black Diamond Therapeutics",
            "Cabaletta Therapeutics",
            "TCR2 Therapeutics",
            "Adaptimmune",
            "AgeX Therapeutics",
            "Blueprint Medicines",
            "Deciphera Therapeutics",
            "Atara Bio",
            "Ideaya Biosciences"
        ]
        @company_details = [
            "CRISPR gene editing therapies for rare diseases and immuno-oncology",
            "CRISPR gene editing therapies for rare diseases and immuno-oncology",
            "CRISPR gene editing therapies for rare diseases and immuno-oncology",
            "CRISPR base editing for rare diseases",
            "Gene therapies for rare diseases and CAR-T for oncology",
            "Gene therapies for hemophilia B and Huntington's",
            "Gene therapy, RNA therapy, and gene editing approaches for rare neuromuscular/CNS diseases like DMD",
            "AAV gene therapy platform for rare and common diseases, including Wet AMD",
            "Gene therapies for inherited retinal diseases and neurological disorders such as Parkinsons",
            "Gene therapies for rare autoimmune disorders",
            "Gene therapies for neurological disorders",
            "Gene therapies for neurological disorders",
            "Gene therapies for rare blood disorders and genetic heart conditions",
            "Hearing loss disorder gene therapies ",
            "Cell therapy platform",
            "Oncology cell therapy iPSC platform",
            "Allogeneic CAR-T platform",
            "Anti-aging senolytics",
            "Anti-aging mTOR modulation",
            "Anti-aging mTOR modulation",
            "Genetically engineered immune cells (non-viral delivery) vs. cancer",
            "Genetically engineered regulatory T cells vs. autoimmune disease",
            "T cell engager therapies vs. ovarian and prostate cancer",
            "Targeted kinase inhibitors vs. HER2, EGFR cancers",
            "Chimeric autoantigen receptor therapies vs autoimmune diseases",
            "Engineered TCR therapies vs. cancer",
            "",
            "Cell therapies for age-related disorders",
            "Targeted kinase inhibitors",
            "Targeted kinase inhibitors",
            "Allogeneic t cell therapies vs. cancer/autoimmune dz",
            "Synthetic lethality/PARP/PARG inhibitors"
        ]
        @selected_publications = UserTopic.where("user_id = ? AND topic_type = 1", current_user.id)
        @selected_companies = UserTopic.where("user_id = ? AND topic_type = 2", current_user.id)
    end
    
    def space_to_underscore(str)
        return str.gsub ' ', '_'
    end

    def deselect_topic
        topic = request.params[:id]
        topic_type = request.params[:topic_type]

        UserTopic.where("user_id = ? AND topic = ?", current_user.id, topic).delete_all
        @button_id = topic.gsub(' ', '_')
        respond_to do |format|
            format.js
        end
    end

    def select_topic
        topic = request.params[:id]
        topic_type = request.params[:topic_type]
        user_topic = UserTopic.new(user_id: current_user.id, topic: topic, topic_type: topic_type)
        user_topic.save

        @button_id = topic.gsub(' ', '_')
        respond_to do |format|
            format.js
        end
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
