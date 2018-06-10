
import json
from io import StringIO

class Login(object):

    def __init__(self, my_requests):
        self.session = my_requests

    def pic_verify(self, get_pic_api, code, pic_verify_api, headers):
        picture = self.session.get(get_pic_api, verify=False)
        with open('code.png', 'wb') as fn:
            fn.write(picture.content)
        picture_index = input('请输入图片验证码序号，英文逗号隔开')
        temp = picture_index.split(',')
        raw_data = StringIO()
        for i in temp:
            raw_data.write(code[i])
            raw_data.write(',')
        raw_data = raw_data.getvalue()
        data = raw_data.rstrip(',')
        submit_data = {'answer': data, 'login_site': 'E', 'rand': 'sjrand'}
        pic_verify_result = self.session.post(pic_verify_api, data=submit_data, headers=headers, verify=False)  # 注意关掉SSL验证
        pic_verify_result_json = json.loads(pic_verify_result.text)
        if pic_verify_result_json['result_code'] == '4':
            return True

    def passwd_verify(self, user_name, password, passwd_verify_api, headers, tk_url, client_url):
        login_data = {'username': user_name, 'password': password, 'appid': 'otn'}
        login_result = self.session.post(passwd_verify_api, data=login_data, headers=headers, verify=False)
        login_result_json = json.loads(login_result.text)
        if login_result_json['result_message'] == '登录成功':
            print('登陆成功')
        yz_data = {'appid':'otn'}
        print('-----------------第一次验证-----------------')
        yz_result = self.session.post(tk_url, data=yz_data, headers=headers, verify=False)
        print(yz_result.text)
        login_message = yz_result.json()['newapptk']
        print('loginMessage=', login_message)
        yz2data = {'tk': login_message}
        yz2_result = self.session.post(client_url, data=yz2data, headers=headers, verify=False)
        print('-----------------第二次验证-----------------')
        if yz2_result.json()['result_code'] == 0:
            return True


