
def order_type(type):
    types = {
        '商务座': '9',
        '特等座': 'P',
        '一等座': 'M',
        '二等座': 'O',
        '高级软卧': '6',
        '软卧': '4',
        '硬卧': '3',
        '软座': '2',
        '硬座': '1',
        '无座': '1',
    }
    return types[type]


# {"1":"成人票","2":"孩票","3":"学生票","4":"伤残军人票"}
# tour_flag:{dc:"dc",wc:"wc",fc:"fc",gc:"gc",lc:"lc",lc1:"l1",lc2:"l2"
# user_name = 18180418701
# password = 15892659700com

# user_name = 13518394413
# password = dx13518394413