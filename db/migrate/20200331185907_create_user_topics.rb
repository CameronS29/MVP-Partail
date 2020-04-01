class CreateUserTopics < ActiveRecord::Migration[6.0]
  def change
    create_table :user_topics do |t|
      t.string :topic
      t.integer :user_id
      t.integer: user_id
      t.timestamps
    end
    add_foreign_key :user_topics, :users
  end
end
