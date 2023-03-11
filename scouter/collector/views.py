from django.http import HttpResponse
from django.shortcuts import render
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, CreateView, UpdateView, ListView

from collector.models import Team, Robot, MatchResult
from collector.tables import TeamTable, MatchResultTable

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

    return render(request, 'collector/team_summary.html', {'team': team})

class MatchCreateView(LoginRequiredMixin, CreateView):
    model = MatchResult
    fields = "__all__"

class RobotCreateView(LoginRequiredMixin, CreateView):
    model = Robot
    fields = "__all__"

class MatchResultListView(ListView):
    model = MatchResult
    fields = "__all__"
    # queryset = MatchResult.objects.all()
    # queryset = MatchResult.objects.order_by('match_number')

    context_object_name = "match_result_list"

def matches(request):
    table = MatchResultTable(MatchResult.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'collector/teams.html', {'table': table})