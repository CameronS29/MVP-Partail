class AddTypeToUserTopics < ActiveRecord::Migration[6.0]
  def change
    add_column :user_topics, :type, :integer
  end
end
