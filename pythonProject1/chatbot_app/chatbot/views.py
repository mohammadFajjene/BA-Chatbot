from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
import sys
sys.path.insert(0, 'C:\\Users\\surface\\PycharmProjects\\pythonProject1')
from chatbot_ import Chatbot
from django.http import JsonResponse



def index(request):
    cs = Chatbot()
    # answer = [
    #     {'ans': 'answer'}
    # ]
    # print(request.POST.get('question'))
    if request.POST and request.is_ajax:
       name = cs.ask(request.POST.get('question'))
       return JsonResponse({'name': name})
    # if request.is_ajax():
    #     html = render_to_string(request, 'chatbot/index.html', {'dishes': answer})
    #     return HttpResponse(html)
    # else:
    return render(request, 'chatbot/index.html')

# Create your views here.
