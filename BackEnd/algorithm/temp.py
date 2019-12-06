'''
不使用数据库，测试算法
'''

import numpy as np
import json


class User(object):
    def __init__(self, cap, his):
        self.capability = cap
        self.ans_history = his

class Question(object):
    def __init__(self, diff):
        self.true_rate = diff
        
def update_cap(user):
    cap = user.capability
    his = user.ans_history


    p = []
    f1, f2 =0, 0
    for que_id in his.keys():
        if his[que_id] == 0:
            continue
        elif his[que_id] == -1:
            his[que_id] == 0
        que = que_id
        diff = que.true_rate
        p.append(1 / (1 + np.exp(-1.7*(cap-diff))))
        f1 += 1.7 * (his[que_id] - p[-1])
        f2 -= 1.7 * p[-1] * (1 - p[-1])
    cap -= f1 / f2
    user.capability = cap

    return

def recommend_que(user, ques):

    #@TODO:存在连续做一道题的可能
    cap = user.capability
    print('cap:'+ str(cap))

    max_info = -1
    for que in ques:
        info = np.exp(cap - que.true_rate) / np.power((1 + np.exp(cap - que.true_rate)), 2)
        print('info' + str(info))
        if info > max_info:
            match_que = que
            max_info = info

    return match_que

q1 = Question(0.1)
q2 = Question(0.2)
q3 = Question(0.3)
q4 = Question(0.4)
q5 = Question(0.5)
q6 = Question(0.6)
q7 = Question(0.7)
q8 = Question(0.8)
q9 = Question(0.9)

u1 = User(0.3, {q1:0, q2:0, q3:1, q4:-1, q5:0, q6:0, q7:0, q8:0, q9:0})

print(recommend_que(u1, [q1, q2, q3, q4, q5, q6, q7, q8, q9]).true_rate)
update_cap(u1)
print(u1.capability)




