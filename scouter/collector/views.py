from django.http import HttpResponse
from django.shortcuts import render
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, CreateView, UpdateView, ListView
import collector.utils as utils

from collector.models import Team, Robot, MatchResult, TeamEfficiency
from collector.tables import TeamTable, MatchResultTable, EfficiencyTable, SummaryResultTable, MatchListTable
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, FormView, CreateView, UpdateView, ListView


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

    # table = MatchResultTable(MatchResult.objects.filter(frc_team=number))
    table = SummaryResultTable(MatchResult.objects.filter(frc_team=number))
    last_three = utils.get_last3_scoring_prediction(number=number)
    last_six = utils.get_last6_scoring_prediction(number=number)
    avg_score = utils.get_team_scoring_prediction(number=number)

    return render(request, 'collector/team_summary.html', {'team': team, 'table': table, 'avg_score': avg_score, 'last_three': last_three, 'last_six': last_six})


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
    table = MatchListTable(MatchResult.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'collector/matches.html', {'table': table})


def update_efficiency_numbers():
    teams = Team.objects.all()

    for team in teams:
        # Try to get their existing efficiency numbers first
        try: 
            team_eff = team.efficiency.get()
        except TeamEfficiency.DoesNotExist:
            team_eff = team.efficiency.create()

        matches = team.matches.all()
        # import pdb
        # pdb.set_trace()
        num_matches = matches.count()

        ONE = 'Really Bad'
        TWO = 'Bad'
        THREE = 'Moderate'
        FOUR = 'Good'
        FIVE = 'Really Good'
        driver_rating_choices = ((ONE, 'Really Bad'), (TWO, 'Bad'), (THREE, 'Average'), (FOUR, 'Good'), (FIVE, 'Great'))

        CLEAN = 'No penalties'
        FEW = 'One or Two penalties'
        MODERATE = 'Multiple Penalties'
        SEVERE = 'A lot of penalties'

        # If there's no match data, just save an empty efficiency
        if num_matches == 0:
            team_eff.save()
        else:
            # Calculate the aggregate of the scores
            auto_pieces_total = 0.0
            auto_charging_total = 0.0
            auto_mobility_total = 0.0
            teleop_low_total = 0.0
            teleop_mid_total = 0.0
            teleop_high_total = 0.0
            engage_attempts_total = 0.0
            endgame_points_total = 0.0
            driver_rating_total = 0.0
            penalty_total = 0.0

            for match in matches:
                if match.auto_mobility:
                    auto_mobility_total += 3
                auto_pieces_total += match.auto_low * 3
                auto_pieces_total += match.auto_mid * 4
                auto_pieces_total += match.auto_high * 6
            
                if match.auto_charge_station == 'Engaged':
                    auto_charging_total += 12
                if match.auto_charge_station == 'Docked':
                    auto_charging_total += 8

                if match.tele_cones_high > 0:
                    teleop_high_total += 5 * match.tele_cones_high

                if match.tele_cubes_mid > 0:
                    teleop_mid_total += 3 * match.tele_cubes_mid
                if match.tele_cones_mid > 0:
                    teleop_mid_total += 3 * match.tele_cones_mid

                if match.tele_cubes_low > 0:
                    teleop_low_total += 2 * match.tele_cubes_low
                if match.tele_cones_high > 0:
                    teleop_low_total += 2 * match.tele_cones_low

                if match.end_scoring == 'Parked':
                    endgame_points_total += 2
                    engage_attempts_total += 1
                if match.end_scoring == 'Docked':
                    endgame_points_total += 6
                    engage_attempts_total += 1
                if match.end_scoring == 'Engaged':
                    endgame_points_total += 10
                    engage_attempts_total += 1
                if match.end_scoring == 'Failed':
                    engage_attempts_total += 1
                if match.driver_rating == ONE:
                    driver_rating_total += 1
                if match.driver_rating == TWO:
                    driver_rating_total += 2
                if match.driver_rating == THREE:
                    driver_rating_total += 3
                if match.driver_rating == FOUR:
                    driver_rating_total += 4
                if match.driver_rating == FIVE:
                    driver_rating_total += 5

                if match.penalties == FEW:
                    penalty_total += 1.5

                if match.penalties == MODERATE:
                    penalty_total += 3

                if match.penalties == SEVERE:
                    penalty_total += 4
                

            # Average the totals across their matches
            team_eff.match_count = num_matches
            team_eff.auto_pieces = auto_pieces_total / num_matches
            team_eff.auto_charging = auto_charging_total / num_matches
            team_eff.auto_mobility = auto_mobility_total / num_matches
            team_eff.teleop_low = teleop_low_total / num_matches
            team_eff.teleop_mid = teleop_mid_total / num_matches
            team_eff.teleop_high = teleop_high_total / num_matches
            team_eff.engage_attempts = engage_attempts_total
            team_eff.endgame_points = endgame_points_total / num_matches
            team_eff.total_points = (endgame_points_total + teleop_high_total + teleop_low_total + teleop_mid_total + auto_pieces_total + auto_charging_total + auto_mobility_total + endgame_points_total) / num_matches
            team_eff.driver_rating = driver_rating_total / num_matches
            team_eff.penalty_rating = penalty_total / num_matches

            team_eff.save()


def efficiency(request):
    
    update_efficiency_numbers()

    efficiency = EfficiencyTable(TeamEfficiency.objects.all())
    RequestConfig(request).configure(efficiency)

    return render(request, 'collector/efficiency.html', {'efficiency': efficiency})


def qualifier_predictor(request, number):
    match = utils.get_qualifier_match(number)

    if match == None:
        return HttpResponse(f"No information found for match: {number}") 

    # We the match
    teams = {}
    match_score = {'auto_points': '2', 'teleop_points': '10', 'endgame_points': '15'}

    team1 = {'number' : match['alliances']['red']['team_keys'][0],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']
    }
    team2 = {'number' : match['alliances']['red']['team_keys'][1],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']

    }
    team3 = {'number' : match['alliances']['red']['team_keys'][2],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']

    }
    team4 = {'number' : match['alliances']['red']['team_keys'][0],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']

    }
    team5 = {'number' : match['alliances']['red']['team_keys'][1],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']

    }
    team6 = {'number' : match['alliances']['red']['team_keys'][2],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']

    }
 
    teams['r1'] = team1
    teams['r2'] = team2
    teams['r3'] = team3
    teams['b1'] = team4
    teams['b2'] = team5
    teams['b3'] = team6

    return render(request, 'scout/predictor_table.html', {'teams': teams})


def match_preview(request, type, number):
    match = utils.get_qualifier_match(number) if type is "q" else utils.get_playoff_match(type, number)

    if match is None:
        return HttpResponse(f"No match data found for match: {type} {number} ")

    teams = {}
    team1 = utils.get_team_scoring_prediction(get_number_from_frckey(frckey=match['alliances']['red']['team_keys'][0]))
    team2 = utils.get_team_scoring_prediction(get_number_from_frckey(frckey=match['alliances']['red']['team_keys'][1]))
    team3 = utils.get_team_scoring_prediction(get_number_from_frckey(frckey=match['alliances']['red']['team_keys'][2]))
    team4 = utils.get_team_scoring_prediction(get_number_from_frckey(frckey=match['alliances']['blue']['team_keys'][0]))
    team5 = utils.get_team_scoring_prediction(get_number_from_frckey(frckey=match['alliances']['blue']['team_keys'][1]))
    team6 = utils.get_team_scoring_prediction(get_number_from_frckey(frckey=match['alliances']['blue']['team_keys'][2]))
    
    teams['r1'] = team1
    teams['r2'] = team2
    teams['r3'] = team3
    teams['b1'] = team4
    teams['b2'] = team5
    teams['b3'] = team6
    return render(request, 'collector/match_preview.html', {'teams': teams})


def get_number_from_frckey(frckey):
    try: 
        team = Team.objects.get(frc_key=frckey)
    except:
        return 0
    return team.number
