from django.apps import AppConfig

# settings.py에 해당 항목을 추가시켜야
# app1을 장고가 인식할수 있게된다.
# DB관련작업에 대한 내용.
# 장고는 models.py를 이용해서 DB 테이블을 생성한다.
# 모델은 앱에 종속되어있다.
class App1Config(AppConfig):
    name = 'app1'
