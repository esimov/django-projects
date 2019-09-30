from django.shortcuts import get_object_or_404, render, HttpResponse

from .models import Board


def index(request):
    boards = Board.objects.all()
    return render(request, 'boards/index.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'boards/topics.html', {'board': board})


def detail(request, board_id):
    html_result = "OK"
    return HttpResponse(html_result)
