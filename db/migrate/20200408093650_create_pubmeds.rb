class CreatePubmeds < ActiveRecord::Migration[6.0]
  def change
    create_table :pubmeds do |t|

      t.timestamps
    end
  end
end
