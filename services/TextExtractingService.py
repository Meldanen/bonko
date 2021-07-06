from datetime import datetime
from random import randrange
import csv
import os


class TextExtractingService:

    def __init__(self, bot):
        self.bot = bot

    async def extract(self, ctx, user_id):
        messages = set()
        while len(messages) < 50:
            print(len(messages))
            guild = ctx.guild
            for channel in guild.text_channels:
                channel_creation = int(channel.created_at.timestamp())
                now = int(datetime.now().utcnow().timestamp())
                random_start = datetime.fromtimestamp(randrange(channel_creation, now))
                async for message in channel.history(limit=11, around=random_start):
                    if message.content:
                        messages.add(message)

        # file_path = 'assets/conversations/giannakis.csv'
        nowUTC = datetime.utcnow()
        nowUTCString = nowUTC.strftime('%Y%m%d%H%M%S%f')[:-3]
        file_path = f'assets/data/{nowUTCString}_all.csv'
        f = open(file_path, "x")
        f.close()
        with open(file_path, mode='w', newline="", encoding='utf-8') as giannakis_conversation:
            giannakis_writer = csv.writer(giannakis_conversation, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            giannakis_writer.writerow(['name', 'line'])
            for message in messages:
                try:
                    # message_content = message.clean_content.encode('utf-8').strip().decode("utf-8")
                    # message_content = message_content.replace(",", " ")
                    user_name = message.author.name.encode('utf-8').strip().decode("utf-8")
                    if "meldan" not in user_name:
                        user_name = "user2"
                    # giannakis_conversation.write(f'{message.author.name},{message.clean_content}\n')
                    giannakis_writer.writerow([user_name, message.clean_content])
                except Exception as e:
                    print(e)
        # giannakis_conversation.close()
        print("Done")

    @staticmethod
    def is_file_empty(file_path):
        return os.path.exists(file_path) and os.stat(file_path).st_size == 0



