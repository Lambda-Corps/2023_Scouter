import django_tables2 as tables
from .models import Team
from django_tables2.utils import A

class TeamTable(tables.Table):
    number = tables.LinkColumn('scout:team_summary', args=[A('number')])
    robot = tables.Column(verbose_name="Robot")

    class Meta:
        model = Team
        template_name = 'django_tables2/bootstrap.html'
        fields = ['number', 'name', 'robot']