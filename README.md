# LokiDiscordChatbot

Loosely following tutorial located here: https://www.freecodecamp.org/news/discord-ai-chatbot/

1. Run `clean_data.py` to create the csv if it is not already there.
2. `pip install -r requirements.txt`
3. `python create_dialog_model.py` or `python create_dialog_model_nv.py` if you have an Nvidia GPU with CUDA installed.
4. `python test_bot.py`

Once the dialog model is complete, create a HuggingFace repository and push the file contents there.

1. `cd ouput-<size>`
2. `pip install huggindface_hub`
3. `huggingface-cli login`
4. `huggindface-cli repo create <name of repo>`
5. `git lfs install`
6. `git remote add origin <link to huggindface repo>`
7. `git lfs migrate import --include="*.bin" --everything`
8. `git add .` & `git commit "message"`
9. `git push origin main`
