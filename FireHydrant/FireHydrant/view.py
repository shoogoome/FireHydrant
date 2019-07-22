

from django.http import HttpResponse

def get(request):
    fp = open('./data/fileauth.txt', 'r')
    a = fp.read()
    fp.close()
    return HttpResponse(a)