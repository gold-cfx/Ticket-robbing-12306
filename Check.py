import configparser


class Ticket(object):

    def __init__(self, my_requests):
        self.session = my_requests

    def get_data(self, ticket_check_api, headers):
        resp = self.session.get(url=ticket_check_api, headers=headers, verify=False)
        data = resp.json()['data']['result']
        return data

    def procces_data(self, data):
        """
        车次-3
        一等座-31
        二等座-30
        硬座-29
        硬卧-28
        软卧-23
        商务座-32
        无座-26
        """
        for my_data in data:
            all_ticket_message = {}
            ticket_message = {}
            val = my_data.split('|')
            ticket_li = val[3]  # ticket_message['车次']
            ticket_message['一等座'] = val[31]
            ticket_message['二等座'] = val[30]
            ticket_message['硬座'] = val[29]
            ticket_message['硬卧'] = val[28]
            ticket_message['软卧'] = val[23]
            ticket_message['商务座'] = val[32]
            ticket_message['无座'] = val[26]
            ticket_message['urldecode'] = val[0]
            ticket_message['train_no'] = val[2]
            all_ticket_message[ticket_li] = ticket_message
            yield all_ticket_message

    @staticmethod
    def check_ticket(generator, *, want_ticket_list, want_type_list):
        for ticket_message in generator:
            for ticket, message in ticket_message.items():
                if ticket in want_ticket_list:
                    for one_type in want_type_list:
                        if message[one_type] != '无' and message[one_type] != '':
                            return ticket, one_type, message['urldecode'], message['train_no']
                        else:
                            return None, None

