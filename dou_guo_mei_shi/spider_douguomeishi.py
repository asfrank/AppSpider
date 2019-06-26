import json
from multiprocessing import Queue
import requests

#创建队列
queue_list = Queue()

def handler_request(url, data):
    header = {
        "client": "4",
        "version": "6941.4",
        "device": "MI 5",
        "sdk": "22,5.1.1",
        "imei": "865166011140236",
        "channel": "baidu",
        # "mac": "8C:EC:4B:7E:31:83",
        "resolution": "1280*720",
        "dpi": "1.5",
        # "android-id": "18cec4b7e3183275",
        # "pseudo-id": "4b7e318327518cec",
        "brand": "Xiaomi",
        "scale": "1.5",
        "timezone": "28800",
        "language": "zh",
        "cns": "3",
        "carrier": "CHINA+MOBILE",
        # "imsi": "460071140236751",
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; MI 5  Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36",
        "act-code": "86ccaf5b812ac3a2e86263ace30cf47b",
        "act-timestamp": "1561463290",
        "uuid": "422826d0-2228-4d49-849e-408c53df0e07",
        "newbie": "1",
        "reach": "10000",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive",
        # "Cookie": "duid=60278029",
        "Host": "api.douguo.net",
        # "Content-Length": "96"
    }
    response = requests.post(url=url, headers=header, data=data)
    return response

def handle_index():
    url = "http://api.douguo.net/recipe/flatcatalogs"
    data = {
        "client": "4",
        # "_session": "1561550962545865166011140236",
        # "v": "1561029447",
        "_vs": "2305",
    }
    response = handler_request(url=url, data=data)
    index_response_dict = json.loads(response.text)
    for index_item in index_response_dict["result"]["cs"]:
        for index_item_1 in index_item["cs"]:
            for item in index_item_1["cs"]:
                data_2 = {
                    "client": "4",
                    # "_session": "1561550962545865166011140236",
                    "keyword": item["name"],
                    "order": "0",
                    "_vs": "400",
                    "type": "0",
                }
                queue_list.put(data_2)

def handle_caipu_list(data):
    print("当前处理的食材是", data["keyword"])
    caipu_list_url = "http://api.douguo.net/recipe/v2/search/0/20"
    caipu_list_response = handler_request(url=caipu_list_url, data=data)
    caipu_list_response_dict = json.loads(caipu_list_response.text)
    for item in caipu_list_response_dict["result"]["list"]:
        caipu_info = {}
        caipu_info["shicai"] = data["keyword"]
        if item["type"] == 13:
            caipu_info["username"] = item["r"]["an"]
            caipu_info["shicai_id"] = item["r"]["id"]
            caipu_info["describe"] = item["r"]["cookstory"].replace("\n","").replace(" ","")
            caipu_info["caipu_name"] = item["r"]["n"]
            caipu_info["zuoliao_list"] = item["r"]["major"]
            print(caipu_info)
        else:
            continue


handle_index()
# print(queue_list.qsize())
handle_caipu_list(queue_list.get())