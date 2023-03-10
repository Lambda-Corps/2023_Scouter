from django.db import models
from django.urls import reverse

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=30, unique=False)
    number = models.IntegerField(primary_key=True, unique=True)
    frc_key = models.CharField(max_length=10, unique=True)

    robot_report = models.OneToOneField('Robot', null=True, on_delete=models.CASCADE, related_name='team', verbose_name="Robot")

    def __str__(self):
        return f"Team {self.number}: {self.name}"
    

class Robot(models.Model):
    NONE = 'None'
    LOW = 'Low Links'
    MID = 'Mid Links'
    HIGH = 'High Links'

    UNTESTED = 'Untested'
    UNRELIABLE = 'Unreliable'
    RELIABLE = 'Reliable'

    SWERVE = 'Swerve'
    WCD = 'West Coast'
    MECANUM = 'Mecanum'

    frc_team = models.OneToOneField(Team, related_name='robot', null=True, on_delete=models.CASCADE,verbose_name="Team")

    tele_goal = ((LOW, 'Low'), (HIGH, 'High'), (MID, 'Mid'), (NONE, 'None'))
    end_game = ((UNTESTED, 'Untested'), (UNRELIABLE, 'Unreliable'), (RELIABLE, 'Reliable'))
    drive_trains = ((SWERVE, 'Swerve'), (WCD, 'West Coast'), (MECANUM, 'Mecanum'))

    # auto points (int field)
    auto_points = models.IntegerField(default=0)

    # drive train type
    drive_type = models.CharField(choices=drive_trains, max_length=12)
    # goal (low/high/mid)
    grid = models.CharField(choices=tele_goal, max_length=11)

    # End Game
    charge_station = models.CharField(choices=end_game, max_length=13)

    def get_absolute_url(self):
        return reverse('collector:team_summary', kwargs={'number': self.frc_team.number})
    
    def __str__(self):
        return f"Expected Auto Score: {self.auto_points}, Drive Train: {self.drive_type}, Preferred grid: {self.grid}, End Game: {self.charge_station}"


class MatchResult(models.Model):
    NONE = 'None'

    AUTO_CS_NONE = 'None'
    AUTO_CS_FAILED = 'Failed'
    AUTO_CS_DOCKED = 'Docked'
    AUTO_CS_ENGAGED = 'Engaged'

    GRID_LOW = 'Low Grid'
    GRID_MID = 'Mid Grid'
    GRID_HIGH = 'High Grid'
    
    TELELOW = 'Low Grid'
    TELEHIGH = 'High Grid'
    TELEMOD = 'Mid Grid'

    PICKUP_GROUND = 'Ground'
    PICKUP_SUB    = 'Substation'
    PICKUP_BOTH   = 'Both'

    END_PARKED = 'Parked'
    END_DOCKED = 'Docked'
    END_ENGAGED = 'Engaged'
    END_FAILED = 'Endgame Failed'
    END_NONE = 'None'

    ONE = 'Really Bad'
    TWO = 'Bad'
    THREE = 'Moderate'
    FOUR = 'Good'
    FIVE = 'Really Good'

    auto_cs_field_choices = ((AUTO_CS_NONE, 'No Auto'), (AUTO_CS_FAILED, 'Failed'), (AUTO_CS_DOCKED, 'Docked'), (AUTO_CS_ENGAGED, 'Engaged'))
    auto_score_field_choices = ((GRID_LOW, 'Low'), (GRID_MID, 'Mid'), (GRID_HIGH, 'High'))
    endgame_cs_field_choices = ((END_NONE, 'None'), (END_FAILED, 'Failed'), (END_DOCKED, 'Docked'), (END_ENGAGED, 'Engaged'), (END_PARKED, 'Parked'))
    tele_score_field_choices = ((GRID_LOW, 'Low'), (GRID_MID, 'Mid'), (GRID_HIGH, 'High'))
    driver_rating_choices = ((ONE, 'Really Bad'), (TWO, 'Bad'), (THREE, 'Average'), (FOUR, 'Good'), (FIVE, 'Great'))

    # Foreign relationship to associate a given match to a specific team
    frc_team = models.ForeignKey(Team, related_name='matches', null=True , on_delete=models.CASCADE)

    # Auto Scoring options
    auto_mobility = models.BooleanField(default=False)
    auto_low = models.IntegerField(default=0)
    auto_mid = models.IntegerField(default=0)
    auto_high = models.IntegerField(default=0)
    auto_attempted = models.IntegerField(default=0)
    auto_scored = models.IntegerField(default=0)
    auto_attempted_cs = models.BooleanField(default=False)
    auto_cs = models.CharField(choices=auto_cs_field_choices, default=AUTO_CS_NONE, max_length=13)

    # Teleop Scoring options
    tele_low = models.IntegerField(default=0)
    tele_mid = models.IntegerField(default=0)
    tele_high = models.IntegerField(default=0)
    tele_attempted = models.IntegerField(default=0)
    tele_scored = models.IntegerField(default=0)
    tele_links = models.IntegerField(default=0)

    # Endgame Scoring options
    end_scoring = models.CharField(choices=endgame_cs_field_choices, default=END_NONE, max_length=15)

    # Driver skill rating (1 - 5)
    driver_rating = models.CharField(choices=driver_rating_choices, default=ONE, max_length=13)

    # Get the url to show the match results
    def get_absolute_url(self):
        return reverse('collector:team_summary', kwargs={'number': self.frc_team.number})

    def __str__(self):
        return f"Match Number: {self.match_number} -- Team Number {self.frc_team.number}"
    
    