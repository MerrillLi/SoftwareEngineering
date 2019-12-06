import numpy as np
import json

def update_cap(use_id):
    '''
    更新一位被试者的能力值，练习时每做完一道题时调用。

    Paramenters
    -----------------
        user_id: str, 被试者的ID（唯一标识符）
    '''
    user = User.objects.get(username=use_id)
    cap = user.capability
    his = json.loads(user.ans_history)

    p = []
    f1, f2 =0, 0
    for que_id in his.keys():
        if his[que_id] == -1:
            continue
        que = Question.objects.get(id=que_id)
        diff = que.true_rate

        p.append(1 / (1 + np.exp(-1.7*(cap-diff))))
        f1 += 1.7 * (his[que_id] - p[-1])
        f2 -= 1.7 * p[-1] * (1 - p[-1])
    new_cap = cap - f1 / f2
    user.capability = new_cap
    user.save()

    return

def recommend_que(user_id):
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
    
    user = User.objects.get(id=user_id)
    cap = user.capability
    low, up = max(cap - 0.3, 0.0), min(cap + 0.3, 1.0)
    ques = list(Question.objects.filter(true_rate__gte=low).filter(true_rate_lte=up))
    if len(ques) == 0:
        ques = list(Question.objects.filter(true_rate__gte=0.0))
    
    max_info = -1
    for que in ques:
        info = np.exp(cap - que.true_rate) / np.power((1 + np.exp(cap - que.true_rate)), 2)
        if info > max_info:
            match_que_id = que.id
            max_info = info

    return match_que_id