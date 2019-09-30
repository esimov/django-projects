from django.shortcuts import HttpResponse
from django.template import loader
from .models import Board


def index(request):
    boards = Board.objects.all()
    template = loader.get_template('boards/index.html')
    context = {
        'boards': boards
    }
    return HttpResponse(template.render(context, request))


def detail(request, board_id):
    html_result = "OK"
    return HttpResponse(html_result)
