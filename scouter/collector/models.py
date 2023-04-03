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

    ROLLER = 'Rollers'
    CLAW = 'Claw'
    BOTH = 'Both'
    PUSH = 'Push Bot'

    CONES = 'Cones'
    CUBES = 'Cubes'
    BOTH_PIECES = 'Cones & Cubes'

    frc_team = models.OneToOneField(Team, related_name='robot', null=True, on_delete=models.CASCADE,verbose_name="Team")

    tele_goal = ((LOW, 'Low'), (HIGH, 'High'), (MID, 'Mid'), (NONE, 'None'))
    end_game = ((UNTESTED, 'Untested'), (UNRELIABLE, 'Unreliable'), (RELIABLE, 'Reliable'), (NONE, 'None'))
    drive_trains = ((SWERVE, 'Swerve'), (WCD, 'West Coast'), (MECANUM, 'Mecanum'))
    manipulator_options = ((PUSH, 'Push Bot'), (CLAW, 'Claw'), (BOTH, 'Both'))
    game_piece_choices = ((CONES, 'Cones'), (CUBES, 'Cubes'), (BOTH_PIECES, 'Cones & Cubes'), (NONE, 'None'))

    # drive train type
    drive_type = models.CharField(choices=drive_trains, max_length=12, default=WCD)

    # manipulator type
    manipulator = models.CharField(choices=manipulator_options, max_length=8, default=NONE)

    # driver experience
    driver_experience = models.IntegerField(default=0)

    # dimensions
    length = models.DecimalField(decimal_places=2, max_digits=4, default=0)
    width = models.DecimalField(decimal_places=2, max_digits=4, default=0)

    # End Game
    charge_station = models.CharField(choices=end_game, max_length=13, default=NONE)

    def get_absolute_url(self):
        return reverse('collector:team_summary', kwargs={'number': self.frc_team.number})
    
    def __str__(self):
        return f"Drive Train: {self.drive_type}, End Game: {self.charge_station}"


class MatchResult(models.Model):
    NONE = 'None'

    AUTO_CS_NONE = 'None'
    AUTO_CS_FAILED = 'Failed'
    AUTO_CS_DOCKED = 'Docked'
    AUTO_CS_ENGAGED = 'Engaged'

    END_PARKED = 'Parked'
    END_DOCKED = 'Docked'
    END_ENGAGED = 'Engaged'
    END_FAILED = 'Endgame Failed'
    END_NONE = 'None'

    CLEAN = 'None'
    ONE = 'One'
    TWO = 'Two'
    SEVERE = 'Three +'

    auto_cs_field_choices = ((AUTO_CS_NONE, 'No Auto'), (AUTO_CS_FAILED, 'Failed'), (AUTO_CS_DOCKED, 'Docked'), (AUTO_CS_ENGAGED, 'Engaged'))
    endgame_cs_field_choices = ((END_NONE, 'None'), (END_FAILED, 'Failed'), (END_DOCKED, 'Docked'), (END_ENGAGED, 'Engaged'), (END_PARKED, 'Parked'))
    driver_penalties = ((CLEAN, 'None'), (ONE, 'One'), (TWO, 'Two'), (SEVERE, 'Three +'))

    # Foreign relationship to associate a given match to a specific team
    frc_team = models.ForeignKey(Team, related_name='matches', null=True , on_delete=models.CASCADE)

    match_number = models.IntegerField(default=0)
    # Auto Scoring options
    auto_mobility = models.BooleanField(default=False)
    auto_low = models.IntegerField(default=0)
    auto_mid = models.IntegerField(default=0)
    auto_high = models.IntegerField(default=0)
    auto_charge_station = models.CharField(choices=auto_cs_field_choices, default=AUTO_CS_NONE, max_length=13)

    # Teleop Scoring options
    tele_low = models.IntegerField(default=0)
    tele_mid = models.IntegerField(default=0)
    tele_high = models.IntegerField(default=0)

    # Endgame Scoring options
    end_scoring = models.CharField(choices=endgame_cs_field_choices, default=END_NONE, max_length=15)

    # Penalties
    penalties = models.CharField(choices=driver_penalties, default=CLEAN, max_length=20)

    # Comments
    comments = models.CharField(default=' ', max_length=255, help_text='(optional)', blank=True)

    # Get the url to show the match results
    def get_absolute_url(self):
        return reverse('collector:team_summary', kwargs={'number': self.frc_team.number})

    def __str__(self):
        return f"Match Number: {self.match_number} -- Team Number {self.frc_team.number}"


class TeamEfficiency(models.Model):
    team = models.ForeignKey(Team, related_name='efficiency', on_delete=models.CASCADE)
    match_count = models.PositiveSmallIntegerField(default=0)
    auto_pieces = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    auto_charging = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    auto_mobility = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    auto_cs_success = models.DecimalField(max_digits=5, decimal_places=2, default=0.0) 
    teleop_low = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    teleop_mid = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    teleop_high = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    teleop_engage_success = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    endgame_points = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total_points = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    penalty_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    