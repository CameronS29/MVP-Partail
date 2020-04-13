class ChangeColumnName < ActiveRecord::Migration[6.0]
  def change
    rename_column :user_topics, :type, :topic_type
  end
end
