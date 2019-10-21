# -*- coding: utf-8 -*-
# coding: utf-8

from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("<h1>粤ICP备19050376号</h1>")




