from pymongo import MongoClient
import pandas as pd

# 実際のパスワードに置き換えてください
password = 'Gl0J9ZXqH2aMPWKT'

# MongoDB Atlasに接続
client = MongoClient(f"mongodb+srv://airaneuro:{password}@cluster0.yiiwykj.mongodb.net/?retryWrites=true&w=majority")

db = client['product_attributes']
collection = db['attributes']

# CSVファイルを読み込む
merged_df = pd.read_csv(
    r'C:\Users\SPMY-172\Documents\Github\python 属性定義\combined_data.csv')  # ファイルのパスを指定してください

# CSVデータをMongoDBにインサート
records = merged_df.to_dict("records")
collection.insert_many(records)

print("Data successfully inserted into MongoDB")
