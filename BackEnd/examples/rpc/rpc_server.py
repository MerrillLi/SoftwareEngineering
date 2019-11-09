#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-10-27 21:51
# @Author : YuHui Li(MerylLynch)
# @File : rpc_server.py
# @Comment : Created By Liyuhui,21:51
# @Completed : No
# @Tested : No

import thriftpy2

from thriftpy2.rpc import make_server

calc_thrift = thriftpy2.load("calc.thrift", module_name="calc_thrift")


class Dispatcher(object):
    def add(self, a, b):
        print("add -> %s + %s" % (a, b))
        return a + b

    def sub(self, a, b):
        print("sub -> %s - %s" % (a, b))
        return a - b

    def mult(self, a, b):
        print("mult -> %s * %s" % (a, b))
        return a * b

    def div(self, a, b):
        print("div -> %s / %s" % (a, b))
        return a // b

    def glist(self, a):
        lst = []
        for i in range(a):
            lst.append(i)
        return lst

    def guser(self, uid):
        user = calc_thrift.userinfo()
        user.uid = uid
        user.name = 'LYH'
        user.addr = 'HY'
        return user


def main():
    server = make_server(calc_thrift.Calculator, Dispatcher(),
                         '127.0.0.1', 6000)
    print("serving...")
    server.serve()


if __name__ == '__main__':
    main()
