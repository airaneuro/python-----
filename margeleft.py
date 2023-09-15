import pandas as pd
import os
import glob
from tqdm import tqdm

path = r'C:\Users\SPMY-172\Documents\Github\python 属性定義\dbdata'
files = glob.glob(path+r'\*.csv')
genre_details_df = pd.read_csv(
    r'C:\Users\SPMY-172\Documents\Github\python 属性定義\dbdata\product_genre_attributes.genre_details.csv', encoding="utf-8")
genres_df = pd.read_csv(
    r'C:\Users\SPMY-172\Documents\Github\python 属性定義\dbdata\product_genre_attributes.genres.csv', encoding="utf-8")

merged_df = pd.merge(genre_details_df, genres_df,
                     left_on='genre_id', right_on='_id', how='left')
merged_df.to_csv('merged.csv', encoding='utf-8_sig', index=None)
