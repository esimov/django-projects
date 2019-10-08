from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:pk>/', views.board_topics, name='topics'),
    path('<int:pk>/new/', views.new_topic, name='new_topic'),
    path('<int:pk>/topics/<int:topic_pk>',
         views.topic_posts, name='topic_posts')
]
