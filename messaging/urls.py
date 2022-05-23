from django.urls import path

from . import views

app_name = 'messages'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.addView, name='add'),
   # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('signup/', views.signup, name='signup'),
    path('user/<int:pk>', views.userView.as_view(), name='user')

]