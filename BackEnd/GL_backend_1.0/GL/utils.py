import numpy as np
import json

def update_cap(username):
    '''
    更新一位被试者的能力值，练习时每做完一道题时调用。

    Paramenters
    -----------------
        user_id: str, 被试者的ID（唯一标识符）
    '''
    user = User.objects.get(username=username)
    cap = user.capability
    his = json.loads(user.ans_history)

    p = []
    f1, f2 =0, 0
    pro_sum = sum(range(len(his.keys())))
    for i, que_id in enumerate(his.keys()):
        if his[que_id] == -1:
            continue
        que = Question.objects.get(id=que_id)
        diff = que.true_rate

        p.append(1 / (1 + np.exp(-1.7*(cap-diff))))
        f1 += i / pro_sum * 1.7 * (his[que_id] - p[-1])
        f2 -= i / pro_sum * 1.7 * p[-1] * (1 - p[-1])
    new_cap = cap - 0.1 * f1 / f2
    user.capability = new_cap
    user.save()

    return

def recommend_que(username):
    '''
    推荐一道最符合能力值的试题，被试者点击下一题时调用。

    Paramenters
    -----------------
        user_id: str, 被试者的ID（唯一标识符）

    return
    -----------------
        match_que_id: str, 最符合能力值试题的题号
    '''
    #@TODO:存在连续做一道题的可能

    user = User.objects.get(username=username)
    cap = user.capability
    his = json.loads(user.ans_history)
    low, up = max(cap - 0.3, 0.0), min(cap + 0.3, 1.0)
    ques = list(Question.objects.filter(true_rate__gte=low).filter(true_rate__lte=up))
    if len(ques) == 0:
        ques = list(Question.objects.filter(true_rate__gte=0.0))

    temp = list(ques)
    for que in ques:    
        if que in his:
            ques.remove(que)
    if len(ques) == 0:
        ques = temp

    max_info = -1
    for que in ques:
        info = np.exp(cap - que.true_rate) / np.power((1 + np.exp(cap - que.true_rate)), 2)
        if info > max_info:
            match_que_id = que.id
            max_info = info

    return match_que_id

def update_his(user, question, flag):
    """
    更新用户做题记录

    Paramenter
    --------------
        user: User, 需要更新的用户
        question: Question, 提交的题目
        flag: str("true"/"false"), 正确与否
    """
    his = json.loads(user.ans_history)
    if len(his) >= 20:
        his.pop(list(his.keys())[0])
    his[question.id] = int(flag == "true")
    user.ans_history = json.dumps(his)
    user.save()
