from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

app = FastAPI()
# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# MongoDBに接続
client = MongoClient("mongodb://localhost:27017/")
db = client['product_genre_attributes']
collection = db['genre_attributes']

# エンドポイントの定義


@app.get("/api/groups")
async def get_groups():
    groups = collection.distinct("ジャンル階層名")
    return {"groups": groups}

# 選択した商品属性定義詳細グループに関連するジャンル階層名を取得


@app.get("/api/groups/{group_name}/genres")
async def get_genres_by_group(group_name: str):
    genres = collection.find({"ジャンル階層名": group_name}).distinct("商品属性定義詳細グループ")
    return {"genres": genres}

# 選択したジャンル階層名に関連する項目名（日本語）を取得


@app.get("/api/genres/{genre_hierarchy}/attributes")
async def get_attributes_by_genre(genre_hierarchy: str):
    attributes = collection.find(
        {"ジャンル階層名": genre_hierarchy}).distinct("項目名（日本語）")
    return {"attributes": attributes}

# 特定の項目名（日本語）の詳細を取得


@app.get("/api/attributes/")
async def get_attribute_details(attribute_name: str, genre: str):
    query = {
        "ジャンル階層名": attribute_name,
        "項目名（日本語）": genre
    }
    print(f"Query: {query}")  # ログ出力
    attribute_details = collection.find_one(query)
    print(f"Result: {attribute_details}")  # ログ出力
    if attribute_details is None:
        return {"error": "Not found"}, 404
    elif attribute_details:
        attribute_details["_id"] = str(attribute_details["_id"])
    return {"attribute_details": attribute_details}