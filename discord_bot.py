from keep_alive import keep_alive

# the os module helps us access environment variables
# i.e., our API keys
import os

# to delay message
import asyncio

# these modules are for querying the Hugging Face model
import json
import requests

# the Discord Python API
import discord

# this is my Hugging Face profile link
API_URL = 'https://api-inference.huggingface.co/models/bhaden94/'


class MyClient(discord.Client):
    def __init__(self, model_name):
        super().__init__()
        self.api_endpoint = API_URL + model_name
        # retrieve the secret API token from the system environment
        huggingface_token = os.environ['HUGGINGFACE_TOKEN']
        # format the header in our request to Hugging Face
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(huggingface_token)
        }

    def query(self, payload):
        """
        make request to the Hugging Face model API
        """
        data = json.dumps(payload)
        response = requests.request('POST',
                                    self.api_endpoint,
                                    headers=self.request_headers,
                                    data=data)
        ret = json.loads(response.content.decode('utf-8'))
        return ret

    async def wait_for_ready(self):
        max_retries = 15
        retries = 0
        while retries < max_retries:
            response = self.query({'inputs': {'text': 'Hello!'}})
            if 'error' not in response:
                break
            retries += 1
            await asyncio.sleep(3)

        return "Your savior is here!"

    async def on_ready(self):
        # print out information when the bot wakes up
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        # send a request to the model without caring about the response
        # just so that the model wakes up and starts loading
        self.query({'inputs': {'text': 'Hello!'}})

    async def on_message(self, message):
        """
        this function is called whenever the bot sees a message in a channel
        """
        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
            return

        # ignore if any other channel besides bots
        if message.channel.name != '🐼┃talk-to-loki':
            return

        # form query payload with the content of the message
        payload = {'inputs': {'text': message.content}}

        # while the bot is waiting on a response from the model
        # set the its status as typing for user-friendliness
        async with message.channel.typing():
            response = self.query(payload)
        bot_response = response.get('generated_text', None)
        was_loading = False

        # we may get ill-formed response if the model hasn't fully loaded
        # or has timed out
        if not bot_response:
            loading_string = "Model bhaden94/LokiDiscordBot-medium is currently loading"
            if 'error' in response:
                if loading_string in response['error']:
                    bot_response = "I am not ready to talk yet. Please wait a minute..."
                    await message.reply(bot_response, mention_author=True)
                    bot_response = await self.wait_for_ready()
                    was_loading = True
                else:
                    print('`Error: {}`'.format(response['error']))
                    bot_response = 'Hmm... something is not right. Please check back in a minute.'
            else:
                bot_response = 'Hmm... something is not right.'

        if was_loading:
            await message.channel.send(bot_response)
            was_loading = False
        else:
            # send the model's response to the Discord channel
            await message.reply(bot_response, mention_author=True)


def main():
    # DialoGPT-medium-joshua is my model name
    client = MyClient('LokiDiscordBot-medium')
    keep_alive()
    client.run(os.environ['DISCORD_TOKEN'])


if __name__ == '__main__':
    main()
