from django.urls import path

from . import views

app_name = 'app1'


urlpatterns = [
    path('', views.index, name='index'),
    #--------------------------21.07.12 detail, answer url 부여
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    #--------------------------21.07.13 질문등록 url부여---------
    path('question/create/', views.question_create, name='question_create')
]