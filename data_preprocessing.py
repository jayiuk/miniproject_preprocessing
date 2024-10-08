import re
import konlpy
import pandas as pd

class data_preprocessing():
    def __init__(self, input):
        self.input = input
    
    def word_prep(self):
        datas = []
        self.input['contents'] = self.input['contents'].astype(str)
        for i_data in self.input['contents']:
            data = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣0-9]', ' ', i_data)
            data = data.split()
            datas.append(data)
        df = pd.DataFrame({'review' : datas})
        return df
    def tokenize(self):
        df = self.word_prep()
        from konlpy.tag import Okt
        kkma = Okt()
        tokens = []
        df['review'] = df['review'].astype(str)
        for reviews in df['review']:
            token_pos = kkma.pos(reviews)
            token = [n for n, tag in token_pos if tag in ["Noun", "Adjective"]]
            tokens.append(token)

        new_df = pd.DataFrame({'review' : tokens})
        point = self.input['point']
        final_df = pd.concat([new_df, point], axis = 1)
        return final_df
