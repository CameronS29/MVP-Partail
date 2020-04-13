# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)
require 'csv'

#csv = CSV.parse(csv_text, :headers => true, :encoding => 'ISO-8859-1', quote_char: "\x00")
CSV.foreach(Rails.root.join('lib/assets/journal_scrape/output/pubmed.csv'), headers: true, col_sep: ?;) do |row|
    t = Pubmed.new
    t.query = row[0]
    t.title = row[1]
    t.url = row[2]
    t.abstract = row[3]
    t.authors = row[4]
    t.date = row[5]
    t.if = row[6]
    t.score = row[7]
    t.journal = row[8]
    t.save
end

CSV.foreach(Rails.root.join('lib/assets/journal_scrape/output/rxivist.csv'), headers: true, col_sep: ?;) do |row|
    t = Rxcist.new
    t.query = row[0]
    t.title = row[1]
    t.url = row[2]
    t.abstract = row[3]
    t.authors = row[4]
    t.date = row[5]
    t.downloads = row[6]
    t.score = row[7]
    t.save
end