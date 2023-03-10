from django.contrib import admin

# Register your models here.
# from .models import MatchResult, Team
from .models import Team, Robot
# admin.site.register(MatchResult)
admin.site.register(Team)
admin.site.register(Robot)