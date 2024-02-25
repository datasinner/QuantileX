from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import Lasso, Ridge
from joblib import dump, load
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from src.entity import ModelTrainerConfig
import pandas as pd


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        self.data_frame = pd.read_csv(
            f"{self.config.data_path}/{self.config.assets_type}.csv"
        )
        self.data_frame["Date"] = pd.to_datetime(self.data_frame["Date"])
        self.data_frame["Close"] = self.data_frame["Close"].shift(-1)
        self.data_frame = self.data_frame.set_index("Date")
        self.last_row = self.data_frame.tail(1).drop("Close", axis=1)
        self.data_frame.drop(self.data_frame.index[-1], inplace=True)
        self.y = self.data_frame["Close"]
        self.X = self.data_frame.drop("Close", axis=1)
        self.metrics = {"MSE": [], "MAE": [], "r2": []}

    def train(self):
        tscv = TimeSeriesSplit(n_splits=5)
        lasso_model = Lasso(alpha=0.1)
        for train_index, test_index in tscv.split(self.X):
            # print(f"Train index: {train_index}")
            X_train, X_test = self.X.iloc[train_index], self.X.iloc[test_index]
            y_train, y_test = self.y.iloc[train_index], self.y.iloc[test_index]

            lasso_model.fit(X_train, y_train)
            predictions = lasso_model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)
            mae = mean_absolute_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)
            print(f"MSE: {mse:.4f}, MAE: {mae:.4f}, R-squared: {r2:.4f}")
            self.metrics["MSE"].append(mse)
            self.metrics["MAE"].append(mae)
            self.metrics["r2"].append(r2)
        dump(
            lasso_model,
            f"{self.config.root_dir}/{self.config.assets_type}/Lasso_for_close.joblib",
        )

    def predict(self):
        loaded_model = load(
            f"{self.config.root_dir}/{self.config.assets_type}/Lasso_for_close.joblib"
        )
        close_prediction = loaded_model.predict(self.last_row)
        close_low = float(close_prediction[0]) - float(self.metrics["MAE"][-1])
        close_high = float(close_prediction[0]) + float(self.metrics["MAE"][-1])
        final_output = {
            "Close_prediction": close_prediction[0],
            "Close_low": close_low,
            "Close_high": close_high,
        }
        df_output = pd.DataFrame([final_output])
        df_output.to_json(
            f"{self.config.output_path}/output_of_{self.config.assets_type}.json",
            orient="records",
            lines=True,
            indent=4,
        )
