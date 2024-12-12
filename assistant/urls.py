from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 메인 페이지
    path('query/', views.get_response, name='get_response'),
]
