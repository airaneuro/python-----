from pymongo import MongoClient

# MongoDBに接続
client = MongoClient("mongodb://localhost:27017/")
db = client['product_genre_attributes']
genres_col = db['genre_details']

# コレクション内の最初のドキュメントを取得
first_doc = genres_col.find_one()

# ドキュメントのフィールド名（キー）を取得
if first_doc:
    field_names = list(first_doc.keys())
    print("Field names in 'genres' collection:", field_names)
else:
    print("No documents found in 'genres' collection.")
