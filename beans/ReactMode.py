class ReactMode:

    def __init__(self, active=False, *emojis):
        self.active = active
        self.emojis = emojis

    def is_active(self):
        return self.active

    def get_emojis(self):
        return self.emojis

    def set_active(self, active):
        self.active = active

    def set_emojis(self, emojis):
        self.emojis = emojis
