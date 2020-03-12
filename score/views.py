import json

import redis
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from score.forms import ClientScoresForm, ClientScoresGetForm
from score.helper import validate_form


class ClientScoresView(View):

    #提交客户端数据
    def post(self, request):
        request_data = json.loads(request.body.decode())
        flag, data = validate_form(
            ClientScoresForm, request_data)
        if not flag:
            return HttpResponse(status=422)
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        r = redis.Redis(connection_pool=pool)
        # pipe = r.pipeline()
        num = r.zadd('new_score1', {data['client_name']: data['score']})
        # result = r.zrange('new_score1', start=0, end=-1, desc=False, withscores=int)
        return HttpResponse(status=201)

    #查询客户端数据
    def get(self, request):
        flag, data = validate_form(
            ClientScoresGetForm, request.GET.dict())
        if not flag:
            return HttpResponse(status=422)
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        r = redis.Redis(connection_pool=pool)
        results = r.zrevrange('new_score1', start=int(data['start']), end=int(data['end']), withscores=True, score_cast_func=int)
        results_list = []
        for result in results:
            rank = r.zrevrank(name='new_score1', value=result[0]) + 1
            tmp_dict = {'rank': rank, 'client_name': result[0].decode(), 'score': int(result[1])}
            results_list.append(tmp_dict)
        input_rank = r.zrevrank(name='new_score1', value=data['client_name'].encode())
        input_rank = None if input_rank is None else input_rank + 1
        input_score = r.zscore(name='new_score1', value=data['client_name'].encode())
        input_score = int(input_score) if input_score else None
        input_dict = {'rank': input_rank, 'client_name': data['client_name'], 'score': input_score}
        results_list.append(input_dict)
        return HttpResponse(results_list)





