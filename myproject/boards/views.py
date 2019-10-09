from django.db.models import Count
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


class PostEditView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'boards/post_edit.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


def index(request):
    boards = Board.objects.all()
    return render(request, 'boards/index.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)

    topics = board.topics.order_by(
        '-last_update').annotate(replies=Count('posts'))
    return render(request, 'boards/topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topics', pk=board.pk)
    else:
        form = NewTopicForm()

    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'boards/topic_posts.html', {'topic': topic})


@login_required
def topic_reply(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=topic.board.pk, topic_pk=topic.pk)
    else:
        form = PostForm()

    return render(request, 'boards/topic_reply.html', {'topic': topic, 'form': form})


def post_edit(request, pk, topic_pk, post_pk):
    post = get_object_or_404(
        Post, topic__board__pk=pk, topic__pk=topic_pk, pk=post_pk)
    return render(request, 'boards/post_edit.html', {'post': post})
