import requests
import discord
import subprocess

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Only runs in the specified text channel
        channel = str(message.channel.name)
        if channel != 'rotas':
            return

        print(f'Message from {message.author}: {message.content}')

        # if message.content.startswith('hey'):
        #     await message.channel.send('Hello World!')

        if len(message.attachments) > 0:
            print('Image found')
            
            image_url = message.attachments[0].url
            print('Image URL: '+image_url)

            data = requests.get(image_url).content
            f = open(image_path,'wb')

            f.write(data) 
            f.close()

            await message.channel.send('Rota recieved! Working on adding it to your calendar now!')

            subprocess.run(["python", "ocr.py"])
            
image_path = 'week_rota.jpg'

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTI2NjA5NTAxNzE2MDYwOTc5Mw.GlkUS9.yOOmvuUyVw3hotlZPEwH2bYyq8EkCcjXAWnHiY')
