from src.constants import *
from src.utils.common import read_yaml, create_directories
from datetime import datetime, timedelta
from src.entity import DataIngestionConfig
from src.entity import DataValidationConfig


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
