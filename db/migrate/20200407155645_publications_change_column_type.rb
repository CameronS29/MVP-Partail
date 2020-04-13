class PublicationsChangeColumnType < ActiveRecord::Migration[6.0]
  def change
    change_column :publications,  :souceid, :string
    change_column :publications,  :title, :string
    change_column :publications,  :type, :string
    change_column :publications,  :state, :string
    change_column :publications,  :issn, :string
    change_column :publications,  :sjr, :string
    change_column :publications,  :sjr_best_quartile, :string
    change_column :publications,  :cites_doc_2, :string
    change_column :publications,  :ref_doc, :string
    change_column :publications,  :country, :string
    change_column :publications,  :publisher, :string
    change_column :publications,  :coverage, :string
    change_column :publications,  :categories, :string
  end
end
