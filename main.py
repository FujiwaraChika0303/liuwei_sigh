# @github-original: https://github.com/y1ndan/genshin-impact-helper

import hashlib
import json
import random
import string
import time
import uuid
import os

from util import log, CONFIG, req


def hexdigest(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


class Base(object):
    def __init__(self, cookies: str = None):
        if not isinstance(cookies, str):
            raise TypeError('%s want a %s but got %s' %
                            (self.__class__, type(__name__), type(cookies)))
        self._cookie = cookies

    def get_header(self):
        header = {
            'User-Agent': CONFIG.USER_AGENT,
            'Referer': CONFIG.REFERER_URL,
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': self._cookie
        }
        return header


class Roles(Base):
    def get_awards(self):
        response = {}
        try:
            response = req.to_python(req.request(
                'get', CONFIG.AWARD_URL, headers=self.get_header()).text)
        except json.JSONDecodeError as e:
            raise Exception(e)

        return response

    def get_roles(self):
        log.info('正在获取账号信息...')
        response = {}
        try:
            response = req.to_python(req.request(
                'get', CONFIG.ROLE_URL, headers=self.get_header()).text)
            message = response['message']
        except Exception as e:
            raise Exception(e)

        if response.get('retcode', 1) != 0 or response.get('data', None) is None:
            raise Exception(message)

        log.info('账号信息已获取')
        return response


class Sign(Base):
    def __init__(self, cookies: str = None):
        super(Sign, self).__init__(cookies)
        self._region_list = []
        self._region_name_list = []
        self._uid_list = []

    @staticmethod
    def get_ds():
        # v2.3.0-web @povsister & @journey-ad
        n = 'h8w582wxwgqvahcdkpvdhbh2w9casgfl'
        i = str(int(time.time()))
        r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
        c = hexdigest('salt=' + n + '&t=' + i + '&r=' + r)
        return '{},{},{}'.format(i, r, c)

    def get_header(self):
        header = super(Sign, self).get_header()
        header.update({
            'x-rpc-device_id': str(uuid.uuid3(uuid.NAMESPACE_URL, self._cookie)).replace('-', '').upper(),
            # 1:  ios
            # 2:  android
            # 4:  pc web
            # 5:  mobile web
            'x-rpc-client_type': '5',
            'x-rpc-app_version': CONFIG.APP_VERSION,
            'DS': self.get_ds(),
        })
        return header

    def get_info(self):
        user_game_roles = Roles(self._cookie).get_roles()
        role_list = user_game_roles.get('data', {}).get('list', [])

        # role list empty
        if not role_list:
            raise Exception(user_game_roles.get('message', 'Role list empty'))

        log.info(f'与当前账号绑定的角色数量: {len(role_list)}')
        info_list = []
        # cn_gf01:  天空岛
        # cn_qd01:  世界树
        self._region_list = [(i.get('region', 'NA')) for i in role_list]
        self._region_name_list = [(i.get('region_name', 'NA')) for i in role_list]
        self._uid_list = [(i.get('game_uid', 'NA')) for i in role_list]

        log.info('正在获取签到信息...')
        for i in range(len(self._uid_list)):
            info_url = CONFIG.INFO_URL.format(
                self._region_list[i], CONFIG.ACT_ID, self._uid_list[i])
            try:
                content = req.request('get', info_url, headers=self.get_header()).text
                info_list.append(req.to_python(content))
            except Exception as e:
                raise Exception(e)

        if not info_list:
            raise Exception('info_list is empty')

        log.info('签到信息已获取')
        return info_list

    def run(self):
        info_list = self.get_info()
        message_list = []

        for i in range(len(info_list)):
            today = info_list[i]['data']['today']
            total_sign_day = info_list[i]['data']['total_sign_day']
            awards = Roles(self._cookie).get_awards()['data']['awards']
            uid = str(self._uid_list[i]).replace(
                str(self._uid_list[i])[2:-2], '*' * len(str(self._uid_list[i])[2:-2]), 1)

            log.info(f'正在为账号内角色签到 {i + 1} / {len(info_list)} ...')
            time.sleep(random.randint(10, 15))

            message = {
                'today': today,
                'region_name': self._region_name_list[i],
                'uid': uid,
                'total_sign_day': total_sign_day,
                'end': '',
            }

            if info_list[i]['data']['is_sign'] is True:
                message['award_name'] = awards[total_sign_day - 1]['name']
                message['award_cnt'] = awards[total_sign_day - 1]['cnt']
                message['status'] = f'角色 {i + 1} / {len(info_list)} 已经签到过了'
                message_list.append(self.message.format(**message))
                continue
            else:
                message['award_name'] = awards[total_sign_day]['name']
                message['award_cnt'] = awards[total_sign_day]['cnt']

            if info_list[i]['data']['first_bind'] is True:
                message['status'] = f'角色 {i + 1} / {len(info_list)}, 请在米游社App进行第一次签到'
                message_list.append(self.message.format(**message))
                continue

            data = {
                'act_id': CONFIG.ACT_ID,
                'region': self._region_list[i],
                'uid': self._uid_list[i]
            }

            try:
                response = req.to_python(req.request(
                    'post', CONFIG.SIGN_URL, headers=self.get_header(),
                    data=json.dumps(data, ensure_ascii=False)).text)
            except Exception as e:
                raise Exception(e)

            code = response.get('retcode', 99999)
            # 0:      success
            # -5003:  already signed in

            if code != 0:
                message_list.append(response)
                continue

            message['total_sign_day'] = total_sign_day + 1
            message['status'] = response['message']
            message_list.append(self.message.format(**message))

        log.info('当前账号所有角色签到已完成\n')

        return ''.join(message_list)

    @property
    def message(self):
        return CONFIG.MESSAGE_TEMPLATE


def show_info(**kwargs):
    status = kwargs.get('status', '')
    msg = kwargs.get('msg', '')
    hide = kwargs.get('hide', '')

    if isinstance(msg, list) or isinstance(msg, dict):
        # msg = self.to_json(msg)
        msg = '\n\n'.join(msg)

    if not hide:
        log.info(f'结果: {status}\n\n{msg}\n')


if __name__ == '__main__':
    log.info('Genshin Auto Sign-in Start\n')
    msg_list = []
    ret = success_num = fail_num = 0

    # If Using Github Actions:
    # Repo -> Settings -> Secrets -> New repository secret (Name = COOKIE, Value = '''the cookie you get''')
    COOKIE = ''  # :param COOKIE: 米游社的COOKIE, 多个账号的COOKIE值之间用 # 号隔开,例如: 1#2#3#4

    # try to get environment variable "COOKIE"
    if os.environ.get('COOKIE', '') != '':
        COOKIE = os.environ['COOKIE']

    cookie_list = COOKIE.split('#')
    log.info(f'账号数量: {len(cookie_list)}\n')

    for n in range(len(cookie_list)):
        log.info(f'正在为账号签到 {n + 1} / {len(cookie_list)} ...')
        try:
            msg = ' ' * 4 + f'账号 {n + 1} / {len(cookie_list)}{Sign(cookie_list[n]).run()}'
            msg_list.append(msg)
            success_num = success_num + 1
        except Exception as e:
            msg = ' ' * 4 + f'账号 {n + 1} / {len(cookie_list)}\nERROR: {e}'
            msg_list.append(msg)
            fail_num = fail_num + 1
            log.error(msg)
            ret = -1
        continue

    show_info(status=f'成功: {success_num} | 失败: {fail_num}', msg=msg_list)
    if ret != 0:
        log.error('TASK INCOMPLETE')
        exit(ret)
    log.info('THE END')
