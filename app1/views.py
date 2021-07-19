from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# views.py의 위치에서 models.py를 찾아서 question을 import 하라는 의미
from .models import Question
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from app1.forms import QuestionForm
#21.07.19 페이징 처리 관련 모듈 import
from django.core.paginator import Paginator



def index(request):
    #request: 외부 사용자의 요청을 받아오는 것
    #render : 템플릿을 로딩할 때 사용
    #redirect: URL로 이동시 사용
    #사용자가 localhost:8000/app1 페이지 접속이라는 요청을 보냈다.
    #view -> urls에 어떤함수를 실행해야 하는지 확인한다.
    #21.07.09 질문 목록 가져오기.
    # view에서 model단에 요청
    # 요청의 내용: 조회(Question 테이블(모델) create_date 컬럼을 기준으로 정렬해서 가져옴 -> 그 걸과를 question_list에 저장

    page = request.GET.get('page', '1')

    question_list = Question.objects.order_by('-create_date')
    # context라는 변수에 딕셔너리 형태로 question_list key와 value를 저장
    # 템플릿단에서 해당 데이터를 쉽게 조회하기 위해

    # 페이징 처리내용
    # 가져온 데이터를 10개씩 보여주라.

    paginator = Paginator(question_list, 10)
    page_obj= paginator.get_page(page)

    context = {'question_list': page_obj}
    # 받은 요청에 대해 (request)
    # app1/question_list.html 탬플릿을 열어주고
    # 해당 탬플릿에 context 값을 전송
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
    # POST 방식인지 GET 방식인지 확인
    # 이유: 단순히 질문등록 페이지를 오픈한 것인지
    # 아니면 질문등록 페이지에 데이터를 입력해서 저장한 것인지를 구분
    if request.method == "POST":
        # forms.py에 설정한 QuestionForm 클래스를 호출
        # request.post: 사용자가 입력한 데이터를 받아와 준다.
        form = QuestionForm(request.POST)
        # 폼에 들어온 값이 올바른 값(정상적인 값)인지를 확인
        if form.is_valid():
            # 저장을 하기 전 잠시 유보.
            # question 변수에 form에서 받아온 데이터는 넣어 두었지만
            # 아직 DB로 저장하지는 않았다.
            question = form.save(commit=False)
            # create_date 컬럼을 따로 입력받지 않은 이유?
            # 질문등록의 날짜 시간의 경우 현재 시간으로 입력받기 위해
            # view에서 처리
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