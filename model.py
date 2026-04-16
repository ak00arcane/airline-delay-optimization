import pandas as pd
from xgboost import XGBRegressor

def train_model(df):
    df['HOUR'] = df['CRS_DEP_TIME'] // 100
    
    X = df[['HOUR', 'DISTANCE']]
    y = df['DEP_DELAY']
    
    model = XGBRegressor()
    model.fit(X, y)
    
    return model


def predict(model, df):
    df['HOUR'] = df['CRS_DEP_TIME'] // 100
    df['predicted_delay'] = model.predict(df[['HOUR', 'DISTANCE']])
    return df