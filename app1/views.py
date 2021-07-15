from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# views.py의 위치에서 models.py를 찾아서 question을 import 하라는 의미
from .models import Question
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from app1.forms import QuestionForm


def index(request):
    #21.07.09 질문 목록 가져오기.
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'app1/question_list.html', context)

def detail(request, question_id):
    #get_object_or_404: 기본키에 해당하는 건이 없다면 404페이지 출력
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'app1/question_detail.html', context)
# 질문등록함수 21.07.13
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(answer_content=request.POST.get('answer_content'), create_date=timezone.now())
    return redirect('app1:detail', question_id=question.id)

def question_create(request):
    # 수정 내용 : GET, POST 방식에 대한 처리
    # question_form으로 들어올때
    # 질문을 등록할때
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('app1:index')
    else:
        form = QuestionForm()
    return render(request, 'app1/question_form.html', {'form': form})
    # context = {'form': form}
    # return render(request, 'app1/question_form.html', context)와 같다.

#0714수정 (기존내용 백업)
# def question_create(request):
#     form = QuestionForm()
#     return render(request, 'app1/question_form.html', {'form': form})

# get 방식 post방식(데이터 전송방식)
# 1. get방식: url에 파라미터를 붙여서 전송하는 방식
#             속도가 빠르다는 장점이 있지만
#             url에 데이터를 실어서 보내기 때문에 보안에 취약하거나
#             그 외 데이터 전송에 여러가지 제한 사항이 있다.
# 2. 포스트 방식 : HTML의 BODY영역에 데이터를 실어 보내는 방식(form)
#                대용량의 데이터를 보낼 수 있고 주소에 실어 보내지 않기 때문에
#                get방식에 비해 보안성 또한 좋다.

# csrf_token: 브라우저에서 작성된 데이터가 올바른 데이터 인지,
#             혹은 진짜 웹 브라우저에서 작성된 데이터인지 판단하는 기능

# <!--템플릿 태그-->
# <!--{% if 요청 받은 값(question_list)%} : question_list가 있을경우-->
# <!--{% for 임시변수 in 요청받은값(딕셔너리 키값) %} : 딕셔너리의 키의 value를-->
# <!--반복하여 순차적으로 임시변수에 대입.-->
# <!--{{ 임시변수.컬럼 }} : for문에 의해 선언된 임시변수의 컬럼출력-->

#
# {{ }} : 데이터와 관련된 내용을 출력할 때 사용되는 탬플릿 태그
# {% %} : 탬플릿 태그의 속성, 문법등을 사용할때 쓰는 태그