from pymongo import MongoClient
import pandas as pd
import glob
import os
from tqdm import tqdm

# Excelファイルのパスを取得
files = glob.glob(
    r'C:\Users\SPMY-172\Documents\Github\python 属性定義\属性定義書\*.xlsx')
print("Found files:", files)

# 事前に定義するヘッダー
headers = [
    "No", "項目名（日本語）", "必須/任意", "入力方式", "推奨値・選択肢の有無",
    "入力フォーマット", "最大文字数", "日付形式", "単位有無", "楽天推奨単位",
    "複数値可不可", "区切り入力最大数", "区切り文字", "説明", "入力例", "商品ページ内同一値登録対象"
]

# MongoDBに接続
client = MongoClient("mongodb://localhost:27017/")
db = client['product_genre_attributes']
genres_col = db['genres']
genre_details_col = db['genre_details']

# 各Excelファイルに対して処理
for file in tqdm(files):
    # ジャンル一覧シートを読み込む
    genre_sheet_data = pd.read_excel(file, sheet_name='ジャンル一覧')
    inserted_ids = genres_col.insert_many(
        genre_sheet_data.to_dict('records')).inserted_ids
    genres_col.insert_many(genre_sheet_data.to_dict('records'))

    # その他のシート名を取得
    xls = pd.ExcelFile(file)
    sheet_names = xls.sheet_names  # 全てのシート名がリストとして返されます
    sheet_names.remove('ジャンル一覧')  # 'ジャンル一覧' シートは除外
    sheet_names.remove('はじめに')  # 'ジャンル一覧' シートは除外
    sheet_names.remove('推奨値シート')  # 'ジャンル一覧' シートは除外

    # 各シートに対して処理
    for idx, sheet_name in enumerate(sheet_names):
        detail_sheet_data = pd.read_excel(
            file, sheet_name=sheet_name, header=None, skiprows=4, usecols=range(len(headers)))
        detail_sheet_data.columns = headers  # ヘッダーを手動で設定
        # ジャンルIDを追加
        detail_sheet_data['genre_id'] = inserted_ids[idx]
        genre_details_col.insert_many(detail_sheet_data.to_dict('records'))

print('---finished work---')
