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
    driver_experience = models.IntegerField(default=0, max_length=1)

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

    CLEAN = 'No penalties'
    FEW = 'One or Two penalties'
    MODERATE = 'Multiple Penalties'
    SEVERE = 'A lot of penalties'

    auto_cs_field_choices = ((AUTO_CS_NONE, 'No Auto'), (AUTO_CS_FAILED, 'Failed'), (AUTO_CS_DOCKED, 'Docked'), (AUTO_CS_ENGAGED, 'Engaged'))
    auto_score_field_choices = ((GRID_LOW, 'Low'), (GRID_MID, 'Mid'), (GRID_HIGH, 'High'))
    endgame_cs_field_choices = ((END_NONE, 'None'), (END_FAILED, 'Failed'), (END_DOCKED, 'Docked'), (END_ENGAGED, 'Engaged'), (END_PARKED, 'Parked'))
    tele_score_field_choices = ((GRID_LOW, 'Low'), (GRID_MID, 'Mid'), (GRID_HIGH, 'High'))
    driver_penalties = ((CLEAN, 'No penalties'), (FEW, 'One or Two penalties'), (MODERATE, 'Multiple penalties'), (SEVERE, 'A lot of penalties'))
    driver_rating_choices = ((ONE, 'Really Bad'), (TWO, 'Bad'), (THREE, 'Average'), (FOUR, 'Good'), (FIVE, 'Great'))

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
    tele_cones_low = models.IntegerField(default=0)
    tele_cubes_low = models.IntegerField(default=0)
    tele_cones_mid = models.IntegerField(default=0)
    tele_cubes_mid = models.IntegerField(default=0)
    tele_cones_high = models.IntegerField(default=0)
    tele_cubes_high = models.IntegerField(default=0)

    # Endgame Scoring options
    end_scoring = models.CharField(choices=endgame_cs_field_choices, default=END_NONE, max_length=15)

    # Disabled
    robot_disabled = models.BooleanField(default=False)

    # Penalties
    penalties = models.CharField(choices=driver_penalties, default=CLEAN, max_length=20)

    # Driver skill rating (1 - 5)
    driver_rating = models.CharField(choices=driver_rating_choices, default=ONE, max_length=13)

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
    teleop_low = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    teleop_mid = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    teleop_high = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    engage_attempts = models.IntegerField(default=0)
    endgame_points = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total_points = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    driver_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    penalty_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    