from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth.models import User

from .models import Board, Topic, Post
from .forms import NewTopicForm


def index(request):
    boards = Board.objects.all()
    return render(request, 'boards/index.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'boards/topics.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO get the logged in user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('topics', pk=board.pk)
    else:
        form = NewTopicForm()

    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})


def detail(request, board_id):
    html_result = "OK"
    return HttpResponse(html_result)
