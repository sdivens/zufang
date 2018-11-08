# -*- coding:utf-8 -*-
import requests


if __name__ == '__main__':
    bizReq = '{"tranCode":"NETL23","busOrderId":"234234"}'
    # bizReq = {};
    param = {"bizRequest":bizReq,"bankResponse":""}

    header={"Content-Type":"application/x-www-form-urlencoded"}
    r = requests.post("http://10.200.1.26:8680/service/bank/callback",param,headers=header)
