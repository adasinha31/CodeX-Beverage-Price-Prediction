import pandas as pd
import numpy as np
import joblib


model =  joblib.load("artifacts/best_model.pkl")
features =  joblib.load("artifacts/features.pkl")
scaler =  joblib.load("artifacts/scaler.pkl")
numerical_cols =  joblib.load("artifacts/numerical_cols.pkl")


def process(input_data):
    df = pd.DataFrame([input_data.values()], columns=input_data.keys())
    df_encoded = encoded_created(df)

    nominal_cols = ['occupation', 'gender', 'current_brand', 'reasons_for_choosing_brands', 'flavor_preference',
                    'purchase_channel', 'packaging_preference', 'typical_consumption_situations']
    df_encoded = pd.get_dummies(df_encoded, columns=nominal_cols)

    for col in features:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    for col in df_encoded.columns:
        if col not in features:
            df_encoded.drop(col, axis=1, inplace=True)

    df_scaled = scale(df_encoded)
    return df_scaled


def scale(df):
    df[numerical_cols] = scaler.transform(df[numerical_cols])
    return df


def encoded_created(df):
    # Creating Age group
    age_bins = [17, 25, 35, 45, 55, 70]
    age_labels = ['18-25', '26-35', '36-45', '46-55', '56-70']

    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)

    df.drop('age', axis=1, inplace=True)

    # Creating cf_ab_score
    df['consume_frequency(weekly)'] = df['consume_frequency(weekly)'].map(
        {'0-2 times': 1, '3-4 times': 2, '5-7 times': 3})
    df['awareness_of_other_brands'] = df['awareness_of_other_brands'].map(
        {'0 to 1': 1, '2 to 4': 2, 'above 4': 3})
    df['cf_ab_score'] = round(df['consume_frequency(weekly)'] / (
            df['consume_frequency(weekly)'] + df['awareness_of_other_brands']), 2)

    # Creating zaf
    df['zone'] = df['zone'].map({'Urban': 3, 'Metro': 4, 'Rural': 1, 'Semi-Urban': 2})
    df['income_levels'] = df['income_levels'].map({'Not Applicable': 0,
                                                   '<10L': 1,
                                                   '10L - 15L': 2,
                                                   '16L - 25L': 3,
                                                   '26L - 35L': 4,
                                                   '> 35L': 5})
    df['zas_score'] = df['zone'] * df['income_levels']

    # Creating brand switching Indicator
    condition = (
            (df['current_brand'] != 'Established') &
            (df['reasons_for_choosing_brands'].isin(['Price', 'Quality']))
    )
    df['bsi'] = np.where(condition, 1, 0)

    # Encoding the categorical columns
    df['preferable_consumption_size'] = df['preferable_consumption_size'].map(
        {'Small (250 ml)': 1, 'Medium (500 ml)': 2, 'Large (1 L)': 3})
    df['health_concerns'] = df['health_concerns'].map(
        {'Low (Not very concerned)': 1, 'Medium (Moderately health-conscious)': 2, 'High (Very health-conscious)': 3})
    df['age_group'] = df['age_group'].map({'18-25': 1, '26-35': 2, '36-45': 3, '46-55': 4, '56-70': 4})
    df['gender'] = df['gender'].map({'Female': 'F', 'Male': 'M'})
    return df


def predict(input_data):
    df_final = process(input_data)
    # Re-ordering features for prediction
    df_final = df_final[features]
    if 'price_range' in df_final.columns:
        df_final = df_final.drop(columns=['price_range'])
    pred = model.predict(df_final)
    return pred
