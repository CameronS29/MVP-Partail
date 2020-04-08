class Add < ActiveRecord::Migration[6.0]
  def change
    add_column :publications,  :rank, :integer
    add_column :publications,  :souceid, :integer
    add_column :publications,  :title, :string
    add_column :publications,  :type, :string
    add_column :publications,  :state, :string
    add_column :publications,  :issn, :string
    add_column :publications,  :sjr, :integer
    add_column :publications,  :sjr_best_quartile, :string
    add_column :publications,  :h_index, :integer
    add_column :publications,  :total_docs_2018, :integer
    add_column :publications,  :total_docs_3years, :integer
    add_column :publications,  :total_refs, :integer
    add_column :publications,  :total_cities_3yaers, :integer
    add_column :publications,  :citable_docs_3years, :integer
    add_column :publications,  :cites_doc_2, :integer
    add_column :publications,  :ref_doc, :integer
    add_column :publications,  :country, :string
    add_column :publications,  :publisher, :string
    add_column :publications,  :coverage, :string
    add_column :publications,  :categories, :string
  end
end
