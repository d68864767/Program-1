import pandas as pd
from src.utils.logger import Logger
from src.utils.utils import load_json_config

class DataPreprocessor:
    def __init__(self, data_config_path='config/project_settings.json'):
        self.logger = Logger().get_logger()
        self.data_config = load_json_config(data_config_path).get('data_preprocessor_settings', {})
        self.data_path = self.data_config.get('data_path', 'data/')
        self.file_extension = self.data_config.get('file_extension', '.csv')
        self.preprocessing_steps = self.data_config.get('preprocessing_steps', [])
        self.data = None

    def load_data(self, file_name):
        """
        Load data from a file into a pandas DataFrame.
        
        :param file_name: Name of the file to load data from.
        :return: pandas DataFrame with the loaded data.
        """
        try:
            file_path = os.path.join(self.data_path, file_name + self.file_extension)
            self.data = pd.read_csv(file_path)
            self.logger.info(f"Data loaded successfully from {file_path}")
        except Exception as e:
            self.logger.error(f"Error loading data from {file_path}: {e}")
            raise e

    def preprocess_data(self):
        """
        Apply preprocessing steps to the data.
        """
        if self.data is None:
            self.logger.error("No data loaded to preprocess")
            raise ValueError("Data must be loaded before preprocessing")

        try:
            for step in self.preprocessing_steps:
                if step == 'remove_nulls':
                    self.data.dropna(inplace=True)
                    self.logger.info("Removed null values from data")
                elif step == 'lowercase':
                    for col in self.data.select_dtypes(include=['object']).columns:
                        self.data[col] = self.data[col].str.lower()
                    self.logger.info("Converted text to lowercase")
                # Add more preprocessing steps as needed
                else:
                    self.logger.warning(f"Preprocessing step '{step}' is not recognized")

            self.logger.info("Data preprocessing completed successfully")
        except Exception as e:
            self.logger.error(f"Error during data preprocessing: {e}")
            raise e

    def save_preprocessed_data(self, file_name):
        """
        Save the preprocessed data to a file.
        
        :param file_name: Name of the file to save the preprocessed data.
        """
        try:
            file_path = os.path.join(self.data_path, file_name + self.file_extension)
            self.data.to_csv(file_path, index=False)
            self.logger.info(f"Preprocessed data saved successfully to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving preprocessed data to {file_path}: {e}")
            raise e

# Example usage:
# preprocessor = DataPreprocessor()
# preprocessor.load_data('raw_dataset')
# preprocessor.preprocess_data()
# preprocessor.save_preprocessed_data('preprocessed_dataset')
