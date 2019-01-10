import os
import json

from wxpy import ensure_one
from wxpy.api.messages.message import Message
from wxpy.api import chats


from new_utils import spider
from .wxaihelp import wx_ai_help


if not os.path.exists('setting.ini'):
    setting = {
        'recv_group': True,
        'recv_mp': True,
        'recv_friend': True,
        'group_blacklist': [],
        'group_white_list': [],
        'mp_blacklist': [],
        'mp_white_list': [],
        'friend_blacklist': [],
        'friend_white_list': [],
    }
    json.dump(setting,open('setting.ini','w'))

setting = json.load(open('setting.ini','r'))


class Command:

    def __init__(self,wx_bot):
        self.friends = wx_bot.friends()
        self.groups = wx_bot.groups()
        self.mps = wx_bot.mps()
        self.setting_command = [
                '@接收好友消息',
                '@屏蔽好友消息',
                '@接收群消息',
                '@屏蔽群消息',
                '@关闭公众号',
                '@接收公众号',
                '@屏蔽',
                '@接收好友',
                '@接收群',
                '@接收公众号'
            ]

        self.administrator = ensure_one(self.friends.search('管理员'))

        # self.msg = msg

        # 初始化各类数据
        self.msg = Message
        self.msg_raw = dict()
        self.sender  = chats.group.Group
        self.msg_content = str()
        self.msg_command = str()
        self.msg_command_content = str()
        self.is_mp = bool()
        self.is_friend = bool()
        self.is_group = bool()



    def manage(self,msg):
        self.msg = msg
        self.msg_raw = msg.raw
        self.msg_content = self.msg_raw.get('Content')


        # 判断消息发送者身份
        self.is_friend = msg.sender in self.friends
        self.is_group = msg.sender in self.groups
        self.is_mp = msg.sender in self.mps

        # 判断消息字符串的第一个字符是否为@,@为指令单位,且指定分割符在字符串中
        if self.msg_content[0] == '@':

            if  '#' in self.msg_content:
                msg_content_split = self.msg_content.split('#')
                self.msg_command = msg_content_split[0]
                self.msg_command_content = msg_content_split[1]
            else:
                self.msg_command = self.msg_content

            self.command()



    def command(self):


        if self.msg_command == '@快递':

            express = spider.GetExpress(self.msg_command_content)
            self.msg.reply(express.get_express())
            return None

        if self.msg_command == '@天气':
            weather = spider.GetCityWeather(self.msg_command_content)
            self.msg.reply(weather.get_weather())
            return None

        # 判断发信人是否为管理员
        if self.msg.sender.puid is self.administrator.puid:

            # 管理员获取帮助信息
            command_content = ['@指令', '指令', '帮助']
            if self.msg_command in command_content:
                self.administrator.send(wx_ai_help)
                return
            if self.msg_command in self.setting_command:
                self.set_setting()
                return

            friend_name = self.msg_command.replace('@','')
            is_friend = self.friends.search(friend_name)
            is_group = self.groups.search(friend_name)
            is_mp = self.mps.search(friend_name)

            if is_friend:
                ensure_one(is_friend).send(self.msg_command_content)

            if is_mp:
                ensure_one(is_mp).send(self.msg_command_content)

            if is_group:
                ensure_one(is_group).send(self.msg_command_content)

            self.administrator.send('禀报小主,消息已发送至对方')
        else:
            self.forward_message()

    def forward_message(self):
        is_forward = False
        message_sender = self.msg.sender.name
        print(message_sender)
        if self.is_mp and (setting['recv_mp'] or message_sender in setting['mp_white_list']) :
            message_type = '公众号'
            is_forward = True
        if self.is_group and (setting['recv_group'] or message_sender in setting['group_white_list']):
            message_type = '群组:{}'.format(message_sender)
            message_sender = self.msg.member.name
            is_forward = True
        if self.is_friend and (setting['recv_friend'] or message_sender in setting['friend_white_list']):
            message_type = '好友'
            is_forward = True
        if is_forward:
            self.msg.forward(chat=self.administrator,
                         prefix='禀报小主\n你有一条来自{}的消息\n发信人:{}\n内容如下:'.format(message_type,message_sender))

    def reply_message(self):
        pass
    def set_setting(self):
        if self.msg_command == '@接收好友消息':
            setting['recv_friend'] = True
        if self.msg_command == '@屏蔽好友消息':
            setting['recv_friend'] = False
        if self.msg_command == '@接收群消息':
            setting['recv_group'] = True
        if self.msg_command == '@屏蔽群消息':
            setting['recv_group'] = False
        if self.msg_command == '@关闭公众号':
            print('设置公众号')
            setting['recv_mp'] = False
        if self.msg_command == '@接收公众号':
            setting['recv_mp'] = True
        if self.msg_command == '@屏蔽':
            friend = self.friends.search(self.msg_command_content)
            mp = self.mps.search(self.msg_command_content)
            group = self.groups.search(self.msg_command_content)
            if friend:
                setting['friend_blacklist'].append(self.msg_command_content)
            if mp:
                setting['mp_blacklist'].append(self.msg_command_content)
            if group:
                setting['group_blacklist'].append(self.msg_command_content)
        if self.msg_command == '@接收好友':
            setting['friend_white_list'].append(self.msg_command_content)
        if self.msg_command == '@接收群':
            setting['group_white_list'].append(self.msg_command_content)
        if self.msg_command == '@接收公众号':
           setting['mp_white_list'].append(self.msg_command_content)
        json.dump(setting,open('setting.ini','w'))
        self.administrator.send('禀报小主,设置已修改!')
