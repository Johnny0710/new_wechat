import wxpy

from tools import callback
while True:
    wxpy_bot = wxpy.Bot(qr_callback=callback.wxpy_qr_call_back,cache_path=True)

    if bool(wxpy_bot.self.user_name):
        break




# wxpy_bot.auto_mark_as_read = True  # 清除手机红点







wxpy_bot.join()

