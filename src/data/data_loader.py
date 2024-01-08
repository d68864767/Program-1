import os
import pandas as pd
from src.utils.logger import Logger
from src.utils.utils import load_json_config

class DataLoader:
    def __init__(self, data_config_path='config/project_settings.json'):
        self.logger = Logger().get_logger()
        self.data_config = load_json_config(data_config_path).get('data_loader_settings', {})
        self.data_path = self.data_config.get('data_path', 'data/')
        self.file_extension = self.data_config.get('file_extension', '.csv')
        self.data = None

    def load_data(self):
        """
        Load data from the specified directory and file extension.
        """
        try:
            files = [f for f in os.listdir(self.data_path) if f.endswith(self.file_extension)]
            data_frames = []
            for file in files:
                file_path = os.path.join(self.data_path, file)
                self.logger.info(f"Loading data from {file_path}")
                if self.file_extension == '.csv':
                    df = pd.read_csv(file_path)
                elif self.file_extension == '.json':
                    df = pd.read_json(file_path)
                else:
                    raise ValueError(f"Unsupported file extension: {self.file_extension}")
                data_frames.append(df)
            self.data = pd.concat(data_frames, ignore_index=True)
            self.logger.info("Data loading complete.")
        except Exception as e:
            self.logger.error(f"Failed to load data: {str(e)}")
            raise

    def get_data(self):
        """
        Get the loaded data.
        
        :return: Loaded data as a pandas DataFrame.
        """
        if self.data is None:
            self.logger.warning("Data has not been loaded yet. Call 'load_data()' first.")
            return None
        return self.data

# Usage example:
# data_loader = DataLoader()
# data_loader.load_data()
# data = data_loader.get_data()
