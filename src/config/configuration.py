from src.constants import *
from src.utils.common import read_yaml, create_directories
from datetime import datetime, timedelta
from src.entity import DataIngestionConfig
from src.entity import DataValidationConfig
from src.entity import DataTransformationConfig
from src.entity import ModelTrainerConfig


class ConfigurationManager:
    def __init__(
        self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir + "/" + config.assets_type])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            assets_type=config.assets_type,
            start_date=config.start_date,
            interval=config.interval,
        )

        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES,
        )

        return data_validation_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path + "/" + self.config.data_ingestion.assets_type,
            assets_type=config.assets_type,
        )

        return data_transformation_config

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.TrainingArguments

        create_directories([config.root_dir + "/" + config.assets_type])
        create_directories([config.output_path])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            output_path=config.output_path,
            assets_type=config.assets_type,
            alpha=params.alpha,
        )
        return model_trainer_config
