import openai
from src.utils.utils import load_json_config
from src.utils.logger import Logger

class OpenAIConnector:
    def __init__(self):
        self.logger = Logger().get_logger()
        self.api_keys = load_json_config('config/api_keys.json')
        self.openai_api_key = self.api_keys.get('openai_api_key')
        if not self.openai_api_key:
            self.logger.error("OpenAI API key is missing. Please check your 'config/api_keys.json' file.")
            raise ValueError("OpenAI API key is missing. Please check your 'config/api_keys.json' file.")
        openai.api_key = self.openai_api_key

    def generate_text(self, prompt, max_tokens=150, temperature=0.7, top_p=1.0, n=1, stop=None, model="text-davinci-003"):
        """
        Generate text using OpenAI's language model.

        :param prompt: The input text prompt to generate text from.
        :param max_tokens: The maximum number of tokens to generate in the completion.
        :param temperature: What sampling temperature to use. Higher values mean the model will take more risks.
        :param top_p: An alternative to sampling with temperature, called nucleus sampling, where the model
                      considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens
                      comprising the top 10% probability mass are considered.
        :param n: How many completions to generate for each prompt.
        :param stop: The sequence where the API will stop generating further tokens.
        :param model: The model to use for the completion.
        :return: The generated text as a string.
        """
        try:
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=n,
                stop=stop
            )
            generated_texts = [completion['text'].strip() for completion in response['choices']]
            return generated_texts if n > 1 else generated_texts[0]
        except openai.error.OpenAIError as e:
            self.logger.error(f"An error occurred while generating text: {str(e)}")
            raise

# Usage example:
# connector = OpenAIConnector()
# generated_text = connector.generate_text("Once upon a time")
# print(generated_text)
