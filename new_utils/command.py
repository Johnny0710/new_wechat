import os
import json

from wxpy import ensure_one
from wxpy.api.messages.message import Message
from wxpy.api import chats


from new_utils import spider
from .wxaihelp import wx_ai_help


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

        # 获取配置文件
        self.setting = json.load(open('setting.ini', 'r'))

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
            return self.admin_cmd()
        else:
            return self.forward_message()

    def admin_cmd(self):

        # 管理员获取帮助信息
        command_content = ['@指令', '指令', '帮助']
        if self.msg_command in command_content:
            self.administrator.send(wx_ai_help)
            return
        # 管理员设置配置文件
        if self.msg_command in self.setting_command:
            self.set_setting()
            return

        # 当以上两条均不符合时,默认为给好友发送消息
        target = self.msg_command.replace('@', '')  # 获取好友名称
        search_friend = self.friends.search(target)     # 查找好友
        search_group = self.groups.search(target)       # 查找群组
        search_mp = self.mps.search(target)            # 查找公众号

        # 判断目标是否为好友/群组/公众号三者之一
        if search_friend or search_group or search_mp:
            if search_friend:
                ensure_one(search_friend).send(self.msg_command_content)

            if search_mp:
                ensure_one(search_mp).send(self.msg_command_content)

            if search_group:
                ensure_one(search_group).send(self.msg_command_content)

            return self.administrator.send('禀报小主,消息已发送至对方')
        else:
            return self.administrator.send('禀报小主,未在您的好友/群组/公众号中查询到此名称,请小主核实后再次尝试哦!')

    def forward_message(self):
        message_type = ''
        is_forward = False
        message_sender = self.msg.sender.name
        # 当发信人为公众号时进行以下潮州
        if self.is_mp:
            # 当允许接收公众号消息,并且当前公众号没有存在于公众号黑名单时对消息进行转发
            if self.setting['recv_mp'] and message_sender not in self.setting['mp_black_list']:
                message_type = '公众号'
                is_forward = True
            # 当拒绝公众号消息时,并且当前公众号存在于公众号白名单中时,对消息进行转发
            if not self.setting['recv_mp']  and message_sender in self.setting['mp_white_list']:
                message_type = '公众号'
                is_forward = True

        # 当 发信人为群消息时,进行以下操作
        if self.is_group:
            # 当允许接收群消息,并且当前群名称没有存在于群黑名单时对消息进行转发
            if self.setting['recv_group'] and message_sender not in self.setting['group_black_list']:
                message_type = '群组:{}'.format(message_sender)
                is_forward = True
            # 当拒绝群消息时,并且当前群名称存在于群白名单中时,对消息进行转发
            if not self.setting['recv_group']  and message_sender in self.setting['group_white_list']:
                message_type = '公众号'
                is_forward = True
        # 当 发信人为好友时,进行以下操作
        if self.is_friend:
            # 当允许好友消息,并且当前好友没有存在于好友黑名单时对消息进行转发
            if self.setting['recv_friend'] and message_sender not in self.setting['friend_black_list']:
                message_type =  '好友'
                is_forward = True
            # 当拒绝好友时,并且当前好友存在于好友白名单中时,对消息进行转发
            if not self.setting['recv_group']  and message_sender in self.setting['friend_white_list']:
                message_type =  '好友'
                is_forward = True

        # 如果是否转发为True 将消息转发至管理员
        if is_forward:
            self.msg.forward(chat=self.administrator,
                         prefix='禀报小主\n你有一条来自{}的消息\n发信人:{}\n内容如下:'.format(
                             message_type,
                             message_sender
                         )
                             )

    def set_setting(self):
        if self.msg_command == '@接收好友消息':
            self.setting['recv_friend'] = True
        if self.msg_command == '@屏蔽好友消息':
            self.setting['recv_friend'] = False
        if self.msg_command == '@接收群消息':
            self.setting['recv_group'] = True
        if self.msg_command == '@屏蔽群消息':
            self.setting['recv_group'] = False
        if self.msg_command == '@关闭公众号':
            self.setting['recv_mp'] = False
        if self.msg_command == '@接收公众号':
            self.setting['recv_mp'] = True
        if self.msg_command == '@屏蔽':
            friend = self.friends.search(self.msg_command_content)
            mp = self.mps.search(self.msg_command_content)
            group = self.groups.search(self.msg_command_content)
            if friend:
                self.setting['friend_blacklist'].append(self.msg_command_content)
            if mp:
                self.setting['mp_blacklist'].append(self.msg_command_content)
            if group:
                self.setting['group_blacklist'].append(self.msg_command_content)
        if self.msg_command == '@接收好友':
            self.setting['friend_white_list'].append(self.msg_command_content)
        if self.msg_command == '@接收群':
            self.setting['group_white_list'].append(self.msg_command_content)
        if self.msg_command == '@接收公众号':
            self.setting['mp_white_list'].append(self.msg_command_content)
        json.dump(self.setting,open('setting.ini','w'))
        self.administrator.send('禀报小主,设置已修改!')
