class RxcistAddColumn < ActiveRecord::Migration[6.0]
  def change
    add_column :rxcists, :query, :string
    add_column :rxcists, :title, :string
    add_column :rxcists, :url, :string
    add_column :rxcists, :abstract, :string
    add_column :rxcists, :authors, :string
    add_column :rxcists, :date, :string
    add_column :rxcists, :score, :string
    add_column :rxcists, :downloads, :string
  end
end
