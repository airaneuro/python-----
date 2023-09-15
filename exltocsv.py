import pandas as pd
import glob
from tqdm import tqdm
import csv
import os

# Excelファイルのパスを取得
files = glob.glob(
    r'C:\\Users\\SPMY-172\\Documents\\Github\\python 属性定義\\属性定義書\\*.xlsx')
print("Found files:", files)

# 事前に定義するヘッダー
headers = [
    "No", "項目名（日本語）", "必須/任意", "入力方式", "推奨値・選択肢の有無",
    "入力フォーマット", "最大文字数", "日付形式", "単位有無", "楽天推奨単位",
    "複数値可不可", "区切り入力最大数", "区切り文字", "説明", "入力例", "商品ページ内同一値登録対象",
    "商品属性定義詳細グループ", "ジャンル階層名"
]

# CSVファイルを開く（ヘッダーを書き込む）
with open('combined_data.csv', 'w', newline='',encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(headers)  # ヘッダーを最初に書き込む

    # 各Excelファイルに対して処理
    for file in tqdm(files):
        # ジャンル一覧シートを読み込む
        genre_sheet_data = pd.read_excel(file, sheet_name='ジャンル一覧')

        # その他のシート名を取得
        xls = pd.ExcelFile(file)
        sheet_names = xls.sheet_names
        sheet_names.remove('ジャンル一覧')
        sheet_names.remove('はじめに')
        sheet_names.remove('推奨値シート')

        # 各シートに対して処理
        for sheet_name in sheet_names:
            #print(sheet_name)

            # 商品属性定義詳細データを読み込む
            detail_sheet_data = pd.read_excel(
                file, sheet_name=sheet_name, header=None, skiprows=4)
            detail_sheet_data.columns = detail_sheet_data.iloc[0]
            detail_sheet_data = detail_sheet_data.drop(0).reset_index(drop=True)

            # 商品属性定義詳細グループの列を追加
            detail_sheet_data['商品属性定義詳細グループ'] = sheet_name

            # ジャンル階層名を追加
            genre_name = genre_sheet_data.loc[
                genre_sheet_data['商品属性定義詳細グループ'] == sheet_name, 'ジャンル階層名'].values[0]
            detail_sheet_data['ジャンル階層名'] = genre_name

            # CSVに書き込む
            detail_sheet_data.to_csv(
                csvfile, header=False, index=False, mode='a',encoding='utf-8')

print('---finished work---')
