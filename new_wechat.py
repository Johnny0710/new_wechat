import os
import json

import wxpy

from new_utils import callback
from new_utils import command
from new_utils import friends_list

# 初始化创建机器人

wx_bot = wxpy.Bot(cache_path=True,qr_callback=callback.qr_callback)
wx_bot.enable_puid('wx_bot_friend.pkl')





cmd = command.Command(wx_bot)


@wx_bot.register()
def message(msg):
    cmd.manage(msg)

wx_bot.join()
