from django.urls import path
from . import views

app_name = 'collector'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('teams/', views.teams, name='teams'),
    path('teams/<int:number>', views.team_summary, name='team_summary'),
    path('matches/', views.matches, name='matches'),
    path('submit_match/', views.MatchCreateView.as_view(), name='submit_match'),
    path('pit_scout/', views.RobotCreateView.as_view(), name='pit_scout'),
]