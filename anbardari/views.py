from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def helloworld(request):
    return HttpResponse('hello world.')
