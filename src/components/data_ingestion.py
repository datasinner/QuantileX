from datetime import datetime, timedelta
from pathlib import Path
from src.entity import DataIngestionConfig
from ta import add_all_ta_features
import yfinance as yf
import pandas as pd
import numpy as np
import os


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.df = None
        self.file_path = (
            self.config.root_dir
            + "/"
            + self.config.assets_type
            + "/"
            + self.config.assets_type
            + "_"
            + self.config.start_date
            + "_"
            + datetime.now().strftime("%Y-%m-%d")
            + ".csv"
        )

    def download_file(self):
        if not os.path.exists(self.file_path):
            ticker_obj = yf.Ticker(self.config.assets_type)
            start_date = datetime.strptime(self.config.start_date, "%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
            df = ticker_obj.history(
                start=start_date, end=end_date, interval=self.config.interval
            )
            self.df = df

    def save_data(self):
        if not os.path.exists(self.file_path):
            self.df.to_csv(self.file_path, index=True)
