import re

from bs4 import BeautifulSoup


class Order(object):

    def __init__(self, my_requests):
        self.session = my_requests

    def check_user(self, url, data, headers):
        result = self.session.post(url, data=data, headers=headers, verify=False)
        print(result.text)
        if result.json()['data']['flag'] == True:
            return True

    def submit_order(self, url, data, headers):
        result = self.session.post(url=url, data=data, headers=headers, verify=False)
        print(result.text)

    def get_submit_token_and_more(self, url, headers):
        response = self.session.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, 'lxml')
        submit_token = soup.html.script.text.split(';')[1].split('=')[1].strip(" ").strip("'")
        left_ticket = re.search("'ypInfoDetail':'(.*?)'", response.text).group(1)
        purpose_codes = re.search("'purpose_codes':'(.*?)'", response.text).group(1)
        train_location = re.search("'train_location':'(.*?)'}", response.text).group(1)
        key_check_is_change = re.search("'key_check_isChange':'(.*?)'", response.text).group(1)
        choose_seats = re.search("choose_Seats=(.*?);",  response.text).group(1)

        print(submit_token, left_ticket, purpose_codes, train_location, key_check_is_change, choose_seats)
        return submit_token, left_ticket, purpose_codes, train_location, key_check_is_change, choose_seats

    def get_person(self, url, data, headers):
        result = self.session.post(url, data=data, headers=headers, verify=False)
        print(result.text)

    def check_order_info(self, url, data, headers):
        result = self.session.post(url, data=data, headers=headers, verify=False)
        print(result.text)

    def get_queue_count(self, url, data, headers):
        result = self.session.post(url, data=data, headers=headers, verify=False)
        print(result.text)

    def confirm_single_for_queue(self, url, data, headers):
        result = self.session.post(url, data=data, headers=headers, verify=False)
        print(result.text)

    def query_order_wait_time(self, url, data, headers):
        result = self.session.get(url, params=data, headers=headers, verify=False)
        print(result.text)
        return result.json()

    def result_order_for_dc_queue(self, url, data, headers):
        result = self.session.post(url, data=data, headers=headers, verify=False)
        print(result.text)
        return result.json()

