import os
import torch
from torch.utils.data import DataLoader
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config, AdamW
from src.utils.logger import Logger
from src.utils.utils import load_json_config, save_json_config
from src.data.data_loader import DataLoader as CustomDataLoader
from src.data.data_preprocessor import DataPreprocessor

class ModelTrainer:
    def __init__(self, model_config_path='config/project_settings.json'):
        self.logger = Logger().get_logger()
        self.model_config = load_json_config(model_config_path).get('model_trainer_settings', {})
        self.model_name = self.model_config.get('model_name', 'gpt2')
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def train(self, epochs, save_model_path):
        self.logger.info("Starting training process...")
        data_loader_settings = self.model_config.get('data_loader_settings', {})
        custom_data_loader = CustomDataLoader(data_loader_settings)
        data = custom_data_loader.load_data()
        data_preprocessor = DataPreprocessor()
        processed_data = data_preprocessor.preprocess_data(data)

        train_dataloader = DataLoader(processed_data, batch_size=self.model_config.get('batch_size', 8), shuffle=True)

        optimizer = AdamW(self.model.parameters(), lr=self.model_config.get('learning_rate', 5e-5))

        self.model.train()
        for epoch in range(epochs):
            self.logger.info(f"Epoch {epoch+1}/{epochs}")
            for batch in train_dataloader:
                inputs, labels = batch['input_ids'].to(self.device), batch['labels'].to(self.device)
                optimizer.zero_grad()
                outputs = self.model(inputs, labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()

            self.logger.info(f"Epoch {epoch+1} finished with loss: {loss.item()}")

            if save_model_path:
                self.save_model(epoch, save_model_path)

        self.logger.info("Training process completed.")

    def save_model(self, epoch, save_model_path):
        model_save_path = os.path.join(save_model_path, f"model_epoch_{epoch}.bin")
        self.logger.info(f"Saving model to {model_save_path}")
        torch.save(self.model.state_dict(), model_save_path)
        self.logger.info("Model saved successfully.")

if __name__ == "__main__":
    project_settings = load_json_config('config/project_settings.json')
    model_trainer_settings = project_settings.get('model_trainer_settings', {})
    epochs = model_trainer_settings.get('epochs', 3)
    save_model_path = model_trainer_settings.get('save_model_path', 'models/')

    model_trainer = ModelTrainer()
    model_trainer.train(epochs, save_model_path)
