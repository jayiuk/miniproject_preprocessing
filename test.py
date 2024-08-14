import pandas as pd
import re
from konlpy.tag import Okt
from data_preprocessing import data_preprocessing

# 사용 예시
input_data = pd.read_csv('./홍대입구역맛집리뷰.csv')
print(input_data)
processor = data_preprocessing(input_data)
result_df = processor.tokenize()
print(result_df)
