from .models import Team, MatchResult, Robot

import urllib3
import certifi
import json
import random

def get_event_json(url):
    accept_header = 'application/json'
    auth_key = 'BJG4S2d2nkSkXikztbXHWBL8riwfb4ghAhUIXJ5dezxxhBpvC8ngqrekG2kjF5JV'
    headers = {
        'accept' : 'application/json',
        'X-TBA-Auth-Key' : auth_key,
        'User-Agent' : '1895_Scouter'
    }

    http = urllib3.PoolManager(ca_certs=certifi.where())
    req = http.request('GET', url, headers)

    return json.loads(req.data.decode('UTF-8'))


def update_event_teams():
    url = "https://www.thebluealliance.com/api/v3/event/2023chcmp/teams/simple"
    teams = get_event_json(url)
    
    for team in teams:
        Team.objects.create(name=team['nickname'], number=team['team_number'], frc_key=team['key'])

    print(f"Found {len(teams)} in response")
    # Team.save()

    # return HttpResponse(teams)


def get_frc_match_json():
    url = 'https://www.thebluealliance.com/api/v3/event/2023chcmp/matches/simple'
    # url = 'https://www.thebluealliance.com/api/v3/event/2022chcmp/matches/simple'

    return get_event_json(url)


def get_qualifier_match(number):
    matches = get_frc_match_json()

    for match in matches:
        if match['comp_level'] == "qm" and match['match_number'] == number:
            return match

    # didn't get a match that hit
    return None


def get_playoff_match(type, number):
    matches = get_frc_match_json()

    for match in matches:
        if match['comp_level'] == type and match['set_number'] == number:
            return match

    # didn't find one
    return None


def get_team_scoring_prediction(number):
    return get_scoring_prediction(team_number=number, match_count=25) # 25 is enough to get them all


def get_last3_scoring_prediction(number):
    return get_scoring_prediction(team_number=number, match_count=3)


def get_last6_scoring_prediction(number):
    return get_scoring_prediction(team_number=number, match_count=6)


def get_scoring_prediction(team_number, match_count):
    matches = {}
    team = {}
    try:
        team = Team.objects.get(number=team_number)
        matches = team.matches.all().order_by('-match_number')[:match_count]

    except Team.DoesNotExist:
        return {'number': 1, 'auto_points': 1, 'auto_success': 0, 'teleop_points': 2, 'endgame_points': 3, 'charge_station_success': 0}
    
    # print(matches)
    match_count = matches.count()

    if match_count == 0:
        # use prediction from pit scout
        return {'number': team.number, 'auto_points': 1, 'auto_success': 0, 'teleop_points': 2, 'endgame_points': 3, 'charge_station_success': 0}
    else:
        # Sum up the matches and give an average
        auto_mobility = 0.0
        auto_cs_attempts = 0
        auto_cs_success = 0
        auto_charging_total = 0.0
        auto_point_total = 0.0


        tele_low = 0.0
        tele_mid = 0.0
        tele_high = 0.0

        engage_attempts = 0
        engage_success = 0

        auto_point_total = 0.0
        auto_success = 0.0
        tele_point_total = 0.0
        endgame_points_total = 0.0
        endgame_success = 0.0


        for match in matches:
            if match.auto_mobility:
                    auto_mobility += 3
            auto_point_total += match.auto_low * 3
            auto_point_total += match.auto_mid * 4
            auto_point_total += match.auto_high * 6

            if match.auto_charge_station != 'None':
                    auto_cs_attempts += 1

            if match.auto_charge_station == 'Engaged':
                auto_charging_total += 12
                auto_cs_success += 1
            if match.auto_charge_station == 'Docked':
                auto_charging_total += 8
                auto_cs_success += 1

            tele_point_total += 5 * match.tele_high
            tele_point_total += 3 * match.tele_mid
            tele_point_total += 2 * match.tele_low

            if match.end_scoring == 'Parked':
                endgame_points_total += 2
            if match.end_scoring == 'Docked':
                endgame_points_total += 6
                engage_attempts += 1
            if match.end_scoring == 'Engaged':
                endgame_points_total += 10
                engage_attempts += 1
                engage_success += 1
            if match.end_scoring == 'Failed':
                engage_attempts += 1

        auto_points = round(auto_point_total/match_count, 2)
        auto_cs_success = round(auto_cs_success / auto_cs_attempts, 2)
        tele_points = round(tele_point_total/match_count, 2)
        endgame_points = round(endgame_points_total / match_count, 2)
        endgame_success = round(engage_success / engage_attempts, 2)

        return {'number': team.number, 'auto_points': auto_points, 'auto_success': auto_cs_success, 'teleop_points': tele_points, 'endgame_points': endgame_points, 'charge_station_success': endgame_success}


def team_match_generator(matches_per_team):
    # Possible field entries
    auto_cs_options = ['None', 'Failed', 'Docked', 'Engaged']
    tele_cs_options = ['None', 'Docked', 'Engaged', 'Failed', 'Parked']
    penalties = ['None', 'One', 'Two', 'Three +']
    teams = Team.objects.all()

    for team in teams:
        for x in range(1, matches_per_team):
            result = MatchResult(frc_team=team,
                                match_number=x,
                                auto_mobility=random.randint(0,1) == 0,
                                auto_low=random.randint(0,1),
                                auto_mid=random.randint(0,1),
                                auto_high=random.randint(0,1),                               
                                auto_charge_station=auto_cs_options[random.randint(0,3)],
                                tele_low=random.randint(0,6),
                                tele_mid=random.randint(0,3),
                                tele_high=random.randint(0,6),
                                end_scoring=tele_cs_options[random.randint(0,4)],
                                penalties=penalties[random.randint(0,3)],
                                comments="Auto-Generated Match"
                                )
            result.save()


def get_random_team():
    teams = Team.objects.all()

    team_numbers = []
    for team in teams:
        team_numbers.append(team.number)

    return Team.objects.get(number=team_numbers[random.randint(0, len(team_numbers))])


def pit_scout_generator():
    tele_goal = ['Low', 'High', 'Both', 'None']
    climb_level = ['Low Bar', 'Middle Bar', 'High Bar', 'Traversal Bar', 'No Climb']
    drive_type_choices = ['WCD', 'Swerve', 'Mechanum', 'KoP Chassis']
    # frc_team = models.OneToOneField(Team, related_name='robot', null=True, on_delete=models.CASCADE,verbose_name="Team")
    # auto_points = models.IntegerField(default=0)
    # drive_type = models.CharField(max_length=45)
    # target = models.CharField(choices=tele_goal, max_length=11)
    # climb = models.CharField(choices=climb_level, max_length=13)

    teams = Team.objects.all()

    for team in teams:
        robot = Robot(
            frc_team=team,
            auto_points=random.randint(0,22),
            drive_type=drive_type_choices[random.randint(0,3)],
            target=tele_goal[random.randint(0,3)],
            climb=climb_level[random.randint(0,4)]
        )

        robot.save()
