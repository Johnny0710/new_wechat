

class SearchFriendsList:
    def __init__(self,wx_bot):
        self.wx_bot = wx_bot
        self.friends = self.wx_bot.wx_bot.friends()
        self.groups = self.wx_bot.wx_bot.groups()
        self.mps = self.wx_bot.wx_bot.mps()

    def update_list(self):
        friends = self.wx_bot.friends()
        groups = self.wx_bot.groups()
        mps = self.wx_bot.mps()
