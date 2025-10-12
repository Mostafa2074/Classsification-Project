import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np

class Preprocessing:

    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def outliers(self):
        num_cols = self.df.select_dtypes(include=["int64", "float64"]).columns
        for i,col in enumerate(num_cols):
            Q1=self.df[col].quantile(0.25)
            Q3=self.df[col].quantile(0.75)
            IQR=Q3-Q1
            lower_bound=Q1-1.5*IQR
            upper_bound=Q3+1.5*IQR
            outliers=self.df[col][(self.df[col]<lower_bound) | (self.df[col]>upper_bound)]

    def feature(self):    
        feature_cols = ['Age', 'Gender',
        'Education',
        'Country',
        'Ethnicity',
        'Nscore',
        'Escore',
        'Oscore',
        'Ascore',
        'Cscore',
        'Impulsive',
        'SS']
        self.x = self.df[feature_cols].copy()
        self.y = self.df['Nicotine'].copy()

    def convert_target(self):
        self.y = self.y.apply(lambda x: 0 if x == 'CL0' else 1)

    def label_encoder(self):
        le = LabelEncoder()
        for col in self.x.columns:
            if self.x[col].dtype == 'object':
                self.x[col] = le.fit_transform(self.x[col])
        if self.y.dtype == 'object':
            self.y = le.fit_transform(self.y)

    def standard_scalar(self):       
        self.scaler = StandardScaler()
        self.x=self.scaler.fit_transform(self.x)

 
