from pymongo import MongoClient
import streamlit as st
import os
from dotenv import load_dotenv

# MongoDBの設定を読み込む
load_dotenv("mongodb_credentials.env")
password = os.environ.get('MONGODB_PASSWORD', 'default_password')
client = MongoClient(f"mongodb+srv://airaneuro:{password}@cluster0.yiiwykj.mongodb.net/?retryWrites=true&w=majority")
db = client['product_attributes']
collection = db['attributes']

# MongoDBにインデックスを作成
collection.create_index("ジャンル階層名")
collection.create_index("項目名（日本語）")

@st.cache_data
def get_distinct_values(field):
    return collection.distinct(field)

@st.cache_data
def search_attribute_details(genre, attribute_name):
    query = {
        "ジャンル階層名": genre,
        "項目名（日本語）": attribute_name
    }
    return collection.find_one(query)

@st.cache_data
def attribute_query(q1, isRequired=None):
    query = {"ジャンル階層名": q1}
    if isRequired:
        query["必須/任意"] = "必須"
    return collection.find(query).distinct("項目名（日本語）")

def main():
    # Streamlit UI
    st.title("属性定義書ナビ")
    genre_hierarchys = st.sidebar.multiselect('ジャンル階層名', get_distinct_values("ジャンル階層名"))

    if genre_hierarchys:
        isRequired = st.sidebar.checkbox('必須/任意')
        attribute_names = st.sidebar.multiselect(
            '項目名', attribute_query(genre_hierarchys[0], isRequired))

        if attribute_names:
            attribute_details = search_attribute_details(genre_hierarchys[0], attribute_names[0])

            if attribute_details:
                attribute_details["_id"] = str(attribute_details["_id"])
                st.table(attribute_details)
            else:
                st.warning("error : Not found 404")

if __name__ == "__main__":
    main()
