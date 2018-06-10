import requests
import bs4
import logging
import os
def getStationNamesVersion():
    # 获取 station_names.js 这个文件最新的版本号
    logging.captureWarnings(True)
    url = "https://kyfw.12306.cn/otn/leftTicket/init"
    station_name_version = "" # 先初始化为 0 , 防止没有获取到的时候不能正常返回
    response = requests.get(url, verify=False)
    content = response.text.encode("UTF-8")
    soup = bs4.BeautifulSoup(content, "html.parser")
    scripts = soup.findAll("script")
    srcs = [] # 保存 HTML 中所有的 script 标签的 src 属性
    for i in scripts:
        try: # 这里使用 try 是因为有的 script 标签并没有 src 这个属性
            src = i['src']
            srcs.append(src)
        except:
            pass
    for i in srcs: # 这里设计地比较有扩展性 , 如果还要获取别的某个文件的版本 , 只需要在循环中添加判断即可
        if "station_name" in i: # 找到含有 station_names 的一条 src
            station_name_version = i.split("station_version=")[1] # 截取版本号
            # print "成功获取到车站信息版本 :" , station_name_version # 打印日志
    return station_name_version
def getUrlForStationNames(station_name_version):
    # 构建用于下载 station_names.js 这个文件的地址
    return "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=" + station_name_version
def downloadFile(url, filename):
    #下载文件并保存到本地
    logging.captureWarnings(True)
    f = open(filename, "a",encoding='GBK')
    f.write(requests.get(url, verify=False).text)
    f.close()
# 获取官网的这个文件的版本
print("正在获取官网的火车站信息文件版本...")
station_names_version = getStationNamesVersion()
print("获取成功 !")
print("官网版本号 : [", station_names_version, "]")
# 比对本地文件
print("正在获取本地缓存文件文件名...")
local_file_name = ""
local_file_version = ""
for filename in os.listdir("./"):
    if filename.endswith("_station_names"):
        local_file_name = filename
if local_file_name != "":
    print("获取成功 ! 本地文件名 : [", local_file_name, "]")
    print("正在解析本地文件版本号...")
    local_file_version = local_file_name.split("_")[0]
    print("本地版本号 : [", local_file_version, "]")
else:
    print("本地没有缓存文件 , 准备开始下载...")
# 下载文件 , 保存文件名以版本开始 (便于下次运行的时候比对)
if local_file_version == "":
    print("官网火车站文件更新 , 正在下载...")
    downloadFile(getUrlForStationNames(station_names_version),
                       station_names_version + "_" + "station_names")
else:
    if local_file_version != station_names_version:
        print("官网火车站文件更新 , 正在下载...")
        downloadFile(getUrlForStationNames(station_names_version),
                           station_names_version + "_" + "station_names")
    else:
        print("本地文件已最新 , 直接使用!")
def getStationCodes(station_name):
    results =[]
    # 读取文件
    station_names = open("./" + station_names_version + "_" + "station_names", "r",encoding='GBK')
    content = station_names.read()
    station_names.close()
    content = content[20:-2]  # 去掉多余的 js 关键字 , 只提取出字符串内容
    stations = content.split("@")[1:]  # 由于这个文件开头就是 '@' , 因此需要去掉第一个元素
    for station in stations:
        fields = station.split("|")
        # station_name_pinyin_simple = fields[0]
        station_name_standard = fields[1]
        station_code = fields[2]
        # station_name_pinyin = fields[3]
        # station_name_pinyin_simple_fuzz = fields[4]
        # station_num = fields[5]
        if station_name==station_name_standard:
            # results=station_code
            results.append({"station_code": station_code, "station_name": station_name_standard})
    return results
# def printStationInfo(station_info):
#     for result in station_info:
#         print("[ %s ] -> [ %s ]" % (result["station_name"], result["station_code"]))
# printStationInfo(getStationCodes('成都'))
