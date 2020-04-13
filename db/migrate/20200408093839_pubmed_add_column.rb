class PubmedAddColumn < ActiveRecord::Migration[6.0]
  def change
    add_column :pubmeds, :query, :string
    add_column :pubmeds, :title, :string
    add_column :pubmeds, :url, :string
    add_column :pubmeds, :abstract, :string
    add_column :pubmeds, :authors, :string
    add_column :pubmeds, :date, :string
    add_column :pubmeds, :if, :string
    add_column :pubmeds, :score, :string
    add_column :pubmeds, :journal, :string
  end
end
