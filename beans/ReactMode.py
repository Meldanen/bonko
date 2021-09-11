class ReactMode:

    def __init__(self, active=False, emoji=None):
        self.active = active
        self.emoji = emoji

    def is_active(self):
        return self.active

    def get_emoji(self):
        return self.emoji

    def set_active(self, active):
        self.active = active

    def set_emoji(self, emoji):
        self.emoji = emoji
