from django.http import HttpResponse
from django.shortcuts import render
from django_tables2 import RequestConfig
from collector.models import Team

from collector.tables import TeamTable
from . import views

# Create your views here.
def home_view(request):
    return render(request, 'collector/home.html')

def teams(request):
    table = TeamTable(Team.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'collector/teams.html', {'table': table})

def team_summary(request, number):
    try:
        team = Team.objects.get(number=number)
    except Team.DoesNotExist:
        return HttpResponse("Team {} not found.".format(number))

    return render(request, 'scout/team_summary.html', {'team': team})