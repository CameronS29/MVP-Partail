# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `rails
# db:schema:load`. When creating a new database, `rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2020_04_19_004100) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "company_scrapings", force: :cascade do |t|
    t.string "company"
    t.string "name"
    t.string "title"
    t.string "link"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "publications", force: :cascade do |t|
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.integer "rank"
    t.string "souceid"
    t.string "title"
    t.string "type"
    t.string "issn"
    t.string "sjr"
    t.string "sjr_best_quartile"
    t.integer "h_index"
    t.integer "total_docs_2018"
    t.integer "total_docs_3years"
    t.integer "total_refs"
    t.integer "total_cities_3yaers"
    t.integer "citable_docs_3years"
    t.string "cites_doc_2"
    t.string "ref_doc"
    t.string "country"
    t.string "publisher"
    t.string "coverage"
    t.string "categories"
  end

  create_table "pubmeds", force: :cascade do |t|
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.string "query"
    t.string "title"
    t.string "url"
    t.string "abstract"
    t.string "authors"
    t.string "date"
    t.string "if"
    t.string "score"
    t.string "journal"
  end

  create_table "rxcists", force: :cascade do |t|
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.string "query"
    t.string "title"
    t.string "url"
    t.string "abstract"
    t.string "authors"
    t.string "date"
    t.string "score"
    t.string "downloads"
  end

  create_table "user_topics", force: :cascade do |t|
    t.string "topic"
    t.integer "user_id"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.integer "topic_type"
  end

  create_table "users", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
  end

  add_foreign_key "user_topics", "users"
end
