class CreateCompanyScrapings < ActiveRecord::Migration[6.0]
  def change
    create_table :company_scrapings do |t|
      t.string :company
      t.string :name
      t.string :title
      t.string :link
      t.timestamps
    end
  end
end
