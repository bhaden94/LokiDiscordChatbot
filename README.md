# LokiDiscordChatbot

Following tutorial located here: https://www.freecodecamp.org/news/discord-ai-chatbot/

1. Run `clean_data.py` to create the csv if it is not already there.
2. `pip install -r requirements.txt`
3. `python create_dialog_model.py` or `python create_dialog_model_nv.py` if you have an Nvidia GPU
4. `python test_bot.py`

Push to HuggingFace
`pip install huggingface_hub`
`huggingface-cli login`
`huggingface-cli repo create LokiDiscordBot-medium`
`git lfs install`
`git clone https://huggingface.co/username/model_name`




MY_MODEL_NAME = 'DialoGPT-small-joshua'
with open('HuggingFace-API-key.txt', 'rt') as f:
  HUGGINGFACE_API_KEY = f.read().strip()
  model.push_to_hub(MY_MODEL_NAME, use_auth_token=HUGGINGFACE_API_KEY)
tokenizer.push_to_hub(MY_MODEL_NAME, use_auth_token=HUGGINGFACE_API_KEY)
