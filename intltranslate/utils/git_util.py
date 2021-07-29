import os
import requests


# 从url中下载文件, 存入path + fielname文件中
def download_file_from_git(url, filename, path):
    # url3 = 'https://gitee.com/wuxiangbin/simpleui/raw/master/zh.json'
    r = requests.get(url + filename)
    filename = os.path.join(os.getcwd(), path + filename)

    with open(filename,'wb') as f:
        f.write(r.content)


