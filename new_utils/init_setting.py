import os
import json


def init_setting():
    '''
    recv_group': True,  # 接收群组消息
    'recv_mp': True,  # 接收公众号消息
    'recv_friend': True,  # 接收好友消息
    'group_blacklist': [],  # 群组黑名单,拒收群组消息
    'group_white_list': [],  # 群组白名单,接收群组消息,当接收群组消息为False时启用
    'mp_blacklist': [],     # 公众号黑名单,拒收公众号消息
    'mp_white_list': [],    # 公众号白名单,当接收公众号消息为False时启用
    'friend_blacklist': [], # 好友黑名单,拒收的好友消息
    'friend_white_list': [], # 好友白名单,当接收好友消息为False时启用
    :return:
    '''
    if not os.path.exists('setting.ini'):
        """
        """
        setting = {
            'recv_group': True,  # 接收群组消息
            'recv_mp': True,  # 接收公众号消息
            'recv_friend': True,  # 接收好友消息
            'group_blacklist': [],  # 群组黑名单,拒收群组消息
            'group_white_list': [],  # 群组白名单,接收群组消息,当接收群组消息为False时启用
            'mp_blacklist': [],     # 公众号黑名单,拒收公众号消息
            'mp_white_list': [],    # 公众号白名单,当接收公众号消息为False时启用
            'friend_blacklist': [], # 好友黑名单,拒收的好友消息
            'friend_white_list': [], # 好友白名单,当接收好友消息为False时启用
        }
        json.dump(setting, open('setting.ini', 'w'))

