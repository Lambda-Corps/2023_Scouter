import django_tables2 as tables
from .models import Team, MatchResult, TeamEfficiency
from django_tables2.utils import A

class TeamTable(tables.Table):
    number = tables.LinkColumn('collector:team_summary', args=[A('number')])
    robot = tables.Column(verbose_name="Robot")

    class Meta:
        model = Team
        template_name = 'django_tables2/bootstrap.html'
        fields = ['number', 'name', 'robot']


class MatchResultTable(tables.Table):
    frc_team = tables.Column(verbose_name="Team")

    class Meta:
        model = MatchResult
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['ID', 'id', ' ID', ' id', 'id ', 'id ']

class MatchListTable(tables.Table):
    frc_team = tables.Column(verbose_name="Team")

    class Meta:
        model = MatchResult
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['id', 'comments']

class SummaryResultTable(tables.Table):
    frc_team = tables.Column(verbose_name="Team")

    class Meta:
        model = MatchResult
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['id', 'Team']


class EfficiencyTable(tables.Table):
    team = tables.LinkColumn('collector:team_summary', args=[A('team.number')])

    class Meta:
        model = TeamEfficiency
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['ID', 'id']