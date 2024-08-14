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
        from konlpy.tag import Kkma
        kkma = Kkma()
        tokens = []
        df['review'] = df['review'].astype(str)
        for reviews in df['review']:
            token_pos = kkma.pos(reviews)
            token = [n for n, tag in token_pos if tag in ["NNG","NNP", "VV"]]
            tokens.append(token)

        new_df = pd.DataFrame({'review' : tokens})
        return new_df
