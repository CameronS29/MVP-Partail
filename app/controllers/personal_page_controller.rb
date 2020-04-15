require 'json'

class PersonalPageController < ApplicationController
    def index
        @selected_publications = UserTopic.where("user_id = ? AND topic_type = 1", current_user.id)
        @selected_companies = UserTopic.where("user_id = ? AND topic_type = 2", current_user.id)
        @topic_type = "1"
        @topic = ""
    end

    def scrapping
        @topic = request.params[:id]
        @topic_type = request.params[:topic_type]
        path = Rails.root.to_s + '/lib/assets'

        print path
        if @topic_type == "1"
            @pubmed = Pubmed.where("query like ?", '%' + @topic + '%')
            @rxcist = Rxcist.where("query like ?", '%' + @topic + '%')
            print @pubmed
        else
            path = path + '/company_scrape/script.py';
            @scrapping_result = `python3 #{path} '#{@topic}'`
            @scrapping_result = eval(@scrapping_result)
        end

        respond_to do |format|
            format.js
        end
    end
end
