#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-11-05 17:07
# @Author : YuHui Li(MerylLynch)
# @File : pydb.py
# @Comment : Created By Liyuhui,17:07
# @Completed : No
# @Tested : No

import pymongo

# 连接服务器
client = pymongo.MongoClient("mongodb://10.39.27.16:27017/", )
# 访问服务器上的user数据库
db = client['user']
# 访问user数据库中的userInfo表
col = db['userInfo']

# # Add
# # 插入一个
col.insert_one({'name': 'Liyuhui', 'no': 2017124046, 'gender': 'male', 'major': 'CS'})
# # 插入一堆
# col.insert_many([{'name': 'Liyuhuiv2', 'no': 2017124033, 'gender': 'male', 'major': 'CS'},
#                  {'name': 'MerylLynch', 'no': 2017124033, 'gender': 'male', 'major': 'ME'}])

# Modify
result = col.update_many({'name': 'Liyuhui', 'major': 'CS'}, {"$set": {'major': 'EE'}})
print(result.matched_count)

result = col.find({'no': 2017124033})
for r in result:
    print(r)
# Search
# 查找一个
col.find_one({'name': 'Liyuhui'})
# 查找多个
res = col.find({'name': 'Liyuhui', 'no': {'$gt': 2017124022}})
print(res)
for r in res:
    print(r)
# 搜索，限制2个
col.find({'no': 2017124033}).limit(2)

# Delete
col.delete_one({'name': 'Liyuhui'})
col.delete_many({'major': 'CS'})
client.close()
