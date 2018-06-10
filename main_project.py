import configparser
import datetime
import time

from Check import Ticket
from Login import Login
import requests
from random import randint
from Order import Order
from get_code import getStationCodes
from urllib.parse import unquote
from book_type import order_type
from bs4 import BeautifulSoup



def main():
    my_from_station = '成都东'  # 地点要精确到站
    my_to_station = '重庆北'
    want_day = '2018-06-15'  # 注意时间格式，例如2018-06-15
    want_ticket_list = ['D2244']  # 列表存储，可以用多个车次
    want_type_list = ['二等座']  # 列表存储，可以用多个类型座位

    book_user_name = '陈发兴'  # 姓名
    book_user_person_num = '50023819940511441X'  # 身份证号码
    # book_user_phone_num = '17300282023'  # 手机号码
    # book_user_type ='成人'  # 身份

    my_from_station_code = getStationCodes(my_from_station)[0]['station_code']
    my_to_station_code = getStationCodes(my_to_station)[0]['station_code']

    target = configparser.ConfigParser()
    target.read('settings.ini')

    target.set('my_message', 'my_from_station', my_from_station_code)
    target.set('my_message', 'my_to_station', my_to_station_code)
    target.set('my_message', 'wangt_day', want_day)

    with open('settings.ini', 'w') as fh:
        target.write(fh)  # 把要修改的节点的内容写到文件中

    user_agent = target.get('sys_message', 'user_agent')
    referer = target.get('sys_message', 'referer')
    referer1 = target.get('sys_message', 'referer1')
    get_pic_api = target.get('sys_message', 'get_pic_api')  # 获取图片验证码
    pic_verify_api = target.get('sys_message', 'pic_verify_api')  # 验证图片验证码
    passwd_verify_api = target.get('sys_message', 'passwd_verify_api')  # 验证用户及用户密码
    tk_url = target.get('sys_message', 'tk_url')  # 登陆后的第一此验证
    client_url = target.get('sys_message', 'client_url')  # 登陆后的第二次验证

    headers = {'User-Agent': user_agent, 'Referer': referer}
    headers1 = {'User-Agent': user_agent, 'Referer': referer1}

    check_user_api = target.get('order', 'check_user')  # 检测用户是否为登陆状态，在点击预定前验证
    submit_order_api = target.get('order', 'submit_order')
    get_submit_token_api = target.get('order', 'get_submit_token')
    get_person_api = target.get('order', 'get_person')
    check_order_info_api = target.get('order', 'check_order_info')
    get_queue_count_api = target.get('order', 'get_queue_count')
    confirm_single_for_queue_api = target.get('order', 'confirm_single_for_queue')
    query_order_wait_time_api = target.get('order', 'query_order_wait_time')
    result_order_for_dc_queue_api = target.get('order', 'result_order_for_dc_queue')

    user_name = target.get('my_message', 'user_name')
    password = target.get('my_message', 'password')
    ticket_check_api = target.get('my_message', 'ticket_check_api')  #

    code = {'1': '40,40', '2': '110,40', '3': '180,40', '4': '260,40', '5': '40,120', '6': '110,120', '7': '180,120', '8': '260,120'}

    session = requests.Session()
    no_session_requests = requests

    login = Login(session)
    check = Ticket(no_session_requests)
    order = Order(session)

    times = 0
    while True:
        if login.pic_verify(get_pic_api, code, pic_verify_api, headers):
            if login.passwd_verify(user_name, password, passwd_verify_api, headers, tk_url, client_url):
                print('登陆并验证成功')
                break
    while True:
        time.sleep(randint(1,3))
        if times % 50 == 0:
            session.get('https://kyfw.12306.cn/otn/leftTicket/init', headers=headers)
            print('刷新cookie')
        print('正在检测车票……')
        data = check.get_data(ticket_check_api, headers)
        gen_ticket_message = check.procces_data(data)
        my_ticket, one_type, url_decode, train_no = check.check_ticket(gen_ticket_message, want_ticket_list=want_ticket_list, want_type_list=want_type_list)
        if my_ticket and one_type:
            print('恭喜！车票检测成功！')
            print(my_ticket, one_type, train_no)
            break
        times += 1
        print(f'已经抢票{times}次')

    my_order_ticket = my_ticket
    my_order_train_no = train_no
    my_order_type = one_type
    url_decode = url_decode

    check_user_data = {'_json_att': ''}
    print('-----------------检测登陆状态-----------------')
    time.sleep(randint(1, 5))
    if order.check_user(check_user_api, check_user_data, headers):
        print('登陆状态--登陆')
        submit_order_data = {
            'secretStr': unquote(url_decode),
            'train_date': want_day,
            'back_train_date': want_day,
            'tour_flag': 'dc',  # 单程
            'purpose_codes': 'ADULT',  # 成人
            'query_from_station_name': my_from_station,
            'query_to_station_name': my_to_station,
            'undefined':''
        }
        print(unquote(url_decode))
        # time.sleep(randint(1, 5))
        print('-----------------提交订单信息-----------------')
        order.submit_order(submit_order_api, submit_order_data, headers)
        # time.sleep(randint(1, 5))
        print('-----------------获取token-----------------')
        submit_token, left_ticket, purpose_codes, train_location, key_check_is_change, choose_seats = order.get_submit_token_and_more(get_submit_token_api, headers)
        get_person_data = {'_json_att': '', 'REPEAT_SUBMIT_TOKEN': submit_token}
        # time.sleep(randint(1, 5))
        print('-----------------获取联系人-----------------')
        order.get_person(get_person_api, get_person_data, headers1)

        # check_order_info_data = {
        #     'cancel_flag': '2',  # 固定值
        #      'bed_level_order_num': '000000000000000000000000000000',  # 固定值
        #      'passengerTicketStr': f'{order_type(my_order_type)},0,1,{book_user_name},1,{book_user_person_num},{book_user_phone_num},N',
        #      'oldPassengerStr': f'{book_user_name},1,{book_user_person_num},1_',
        #      'tour_flag': 'dc',
        #      'randCode':'',
        #      'whatsSelect': '1',
        #      '_json_att':'',
        #      'REPEAT_SUBMIT_TOKEN': submit_token,
        # }
        check_order_info_data = {
            'cancel_flag': '2',  # 固定值
            'bed_level_order_num': '000000000000000000000000000000',  # 固定值
            'passengerTicketStr': f'{order_type(my_order_type)},0,1,{book_user_name},1,{book_user_person_num},,N',
            'oldPassengerStr': f'{book_user_name},1,{book_user_person_num},1_',
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': submit_token,
        }

        time.sleep(randint(1, 5))
        print('-----------------检测选票人信息-----------------')
        order.check_order_info(check_order_info_api, check_order_info_data, headers1)

        train_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(want_day, '%Y-%m-%d'))).strftime(
            '%a %b %d %Y %H:%M:%S GMT+0800')
        get_queue_count_data = {
            'train_date': f'{train_date} (中国标准时间)',
            'train_no': my_order_train_no,
            'stationTrainCode': my_order_ticket,
            'seatType': order_type(my_order_type),
            'fromStationTelecode': my_from_station_code,
            'toStationTelecode': my_to_station_code,
            'leftTicket': left_ticket,
            'purpose_codes': purpose_codes,
            'train_location': train_location,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': submit_token,
        }
        # time.sleep(randint(1, 5))
        print('-----------------提交订单-----------------')
        order.get_queue_count(get_queue_count_api, get_queue_count_data, headers1)

        # confirm_single_for_queue_data = {
        #     'passengerTicketStr':f'{order_type(my_order_type)},0,1,{book_user_name},1,{book_user_person_num},{book_user_phone_num},N',
        #     'oldPassengerStr':f'{book_user_name},1,{book_user_person_num},1_',
        #     'randCode':'',
        #     'purpose_codes':purpose_codes,
        #     'key_check_isChange':key_check_is_change,
        #     'leftTicketStr':left_ticket,
        #     'train_location':train_location,
        #     'choose_seats':choose_seats if choose_seats != 'null' else '',
        #     'seatDetailType':'000',
        #     'whatsSelect':'1',
        #     'roomType':'00',
        #     'dwAll':'N',
        #     '_json_att':'',
        #     'REPEAT_SUBMIT_TOKEN': submit_token
        # }
        confirm_single_for_queue_data = {
            'passengerTicketStr': f'{order_type(my_order_type)},0,1,{book_user_name},1,{book_user_person_num},,N',
            'oldPassengerStr': f'{book_user_name},1,{book_user_person_num},1_',
            'randCode': '',
            'purpose_codes': purpose_codes,
            'key_check_isChange': key_check_is_change,
            'leftTicketStr': left_ticket,
            'train_location': train_location,
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': submit_token
        }
        time.sleep(randint(1, 5))
        print('-----------------确认订单-----------------')
        order.confirm_single_for_queue(confirm_single_for_queue_api, confirm_single_for_queue_data, headers1)
        query_order_wait_time_data = {
            'random': str(int(time.time()*1000)),
            'tourFlag': 'dc',
            '_json_att':'',
            'REPEAT_SUBMIT_TOKEN': submit_token,
        }
        print('-----------------排队等待-----------------')
        n = 0
        while True:
            if n <= 2:
                result = order.query_order_wait_time(query_order_wait_time_api, query_order_wait_time_data, headers1)
                if result['data']['waitTime'] == -1 and result['data']['orderId'] !='':
                    global order_id
                    order_id = result['data']['orderId']
                    print(order_id)
                    print('出票成功')
                    break
                else:
                    time.sleep(4)
                n += 1
            else:
                time.sleep(200)
                resp = session.get('https://kyfw.12306.cn/otn/queryOrder/initNoCompleteQueue')
                soup = BeautifulSoup(resp.text, 'lxml')
                try:
                    a = soup.find_all('div', {'class': 'r-txt'})[0].find('h3').text
                except:
                    a = 'jjjj'
                if a =='未出票，订单排队中...':
                    print('正在出票，200后刷新网页')
                    continue
                else:
                    print('出票成功2')
                    break


        result_order_for_dc_queue_data = {
            'REPEAT_SUBMIT_TOKEN': submit_token,
            '_json_att': '',
            'orderSequence_no': order_id
        }
        print('-----------------订单结果-----------------')
        print(result_order_for_dc_queue_data)
        end_result =order.result_order_for_dc_queue(result_order_for_dc_queue_api, data=result_order_for_dc_queue_data, headers=headers1)
        if end_result['status'] and  end_result['data']['submitStatus']:
            print('抢票成功')
        else:
            print('抢票失败')


if __name__ == '__main__':
    main()
