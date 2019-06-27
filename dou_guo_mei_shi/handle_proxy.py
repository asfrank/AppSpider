import requests

url = 'http://ip.hahado.cn/ip'
proxy = {'http':'http://H211EATS905745KC:F8FFBC929EB7D5A7@http-cla.abuyun.com:9030'}
response = requests.get(url=url, proxies=proxy)
print(response.text)