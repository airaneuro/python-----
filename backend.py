from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from bson import json_util
import json
from bson import ObjectId

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = MongoClient("mongodb://localhost:27017/")
db = client['product_genre_attributes']
genres_col = db['genres']
genre_details_col = db['genre_details']


def convert_objectid(genres):
    for genre in genres:
        genre["_id"] = str(genre["_id"])
    return genres


@app.get("/genres/")
async def read_genres():
    genres = list(genres_col.find({}))
    genres = convert_objectid(genres)  # ObjectIdをstrに変換
    return {"genres": genres}


@app.get("/genre_details/{genre_id}")
async def read_genre_details(genre_id: str):
    details = list(genre_details_col.find({"genre_id": ObjectId(genre_id)}))
    return json.loads(json_util.dumps({"details": details}))


@app.get("/genre_details/search/")
async def search_genre_details(group_name: str):
    # 部分一致検索を行うために正規表現を使用
    regex_pattern = f".*{group_name}.*"
    details = list(genre_details_col.find(
        {"ジャンルID": {"$regex": regex_pattern, "$options": "i"}}))
    return json.loads(json_util.dumps({"details": details}))
