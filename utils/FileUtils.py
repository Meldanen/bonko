import discord


def get_file(path):
    with open(path, 'rb') as f:
        picture = discord.File(f)
        return picture
