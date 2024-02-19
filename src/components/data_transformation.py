import os
from src.logging import logger
from datetime import datetime
from src.entity import DataTransformationConfig
from ta import add_all_ta_features
import numpy as np
import pandas as pd


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.df = pd.read_csv(
            self.config.data_path
            + "/"
            + self.config.assets_type
            + "_2015-01-01_"
            + datetime.now().strftime("%Y-%m-%d")
            + ".csv"
        )
        self.preprocessed_df = None
        self.continuous_cols = []
        self.categorical_cols = []

    def preprocess(self):
        preprocessed_df = self.df.copy()
        preprocessed_df["Date"] = pd.to_datetime(preprocessed_df["Date"])
        preprocessed_df = preprocessed_df.set_index("Date")
        preprocessed_df["Timestamp"] = preprocessed_df.index.astype(np.int64) // 10**9
        preprocessed_df["Year"] = preprocessed_df.index.year
        preprocessed_df["Month"] = preprocessed_df.index.month
        preprocessed_df["Day"] = preprocessed_df.index.day
        preprocessed_df["DayOfWeek"] = preprocessed_df.index.dayofweek
        preprocessed_df["MA7_Close"] = preprocessed_df["Close"].rolling(window=7).mean()
        preprocessed_df["MA30_Close"] = (
            preprocessed_df["Close"].rolling(window=30).mean()
        )
        preprocessed_df["Lag1_Close"] = preprocessed_df["Close"].shift(1)
        preprocessed_df["Volume_Change_Pct"] = preprocessed_df["Volume"].pct_change()
        preprocessed_df["target"] = np.where(
            preprocessed_df["Close"] < preprocessed_df["Open"], 0, 1
        )
        preprocessed_df["target"] = preprocessed_df["target"].shift(-1)

        preprocessed_df_with_ta = add_all_ta_features(
            preprocessed_df,
            open="Open",
            high="High",
            low="Low",
            close="Close",
            volume="Volume",
        )

        preprocessed_df_with_ta = self.drop_cols(preprocessed_df_with_ta)

        self.preprocessed_df = preprocessed_df_with_ta

    def identify_column_type(self, threshold_unique=100):

        for col in self.preprocessed_df.columns:
            unique_values = self.preprocessed_df[col].nunique(dropna=False)
            has_floats = any(
                self.preprocessed_df[col].apply(lambda x: isinstance(x, float))
            )
            if has_floats:
                self.continuous_cols.append(col)
                continue
            if unique_values <= threshold_unique:
                self.categorical_cols.append(col)
            else:
                self.continuous_cols.append(col)

    def impute_missing_values(self):
        for continuous_col in self.continuous_cols:
            self.preprocessed_df[continuous_col].fillna(
                self.preprocessed_df[continuous_col].mean(), inplace=True
            )
        for cotegorical_col in self.categorical_cols:
            mode_value = self.preprocessed_df[cotegorical_col].mode()[0]
            self.preprocessed_df[cotegorical_col].fillna(mode_value, inplace=True)

    def drop_cols(self, df):
        for column in df.columns:
            max_count = df[column].value_counts().max()
            if max_count / len(df) > 0.8:
                df.drop(column, axis=1, inplace=True)
        return df

    def save_data(self):
        if not os.path.exists(self.config.root_dir):
            os.makedirs(self.config.root_dir)

        filepath = os.path.join(self.config.root_dir, f"{self.config.assets_type}.csv")
        self.preprocessed_df.to_csv(filepath, index=True)
        print(f"Data saved successfully to {filepath}")

    def convert(self):
        self.preprocess()
        self.identify_column_type()
        self.impute_missing_values()
        self.save_data()
