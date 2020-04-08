class CreateRxcists < ActiveRecord::Migration[6.0]
  def change
    create_table :rxcists do |t|

      t.timestamps
    end
  end
end
