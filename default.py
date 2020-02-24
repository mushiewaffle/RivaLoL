import datetime

import random

import cassiopeia as cass
from cassiopeia import ProfileIcons
from cassiopeia import Summoner, Champion, Champions, ChampionMastery

from random import seed
from random import randint

from PIL import Image

cass.set_riot_api_key("RGAPI-2e399e57-dbf7-462b-9310-e8af37176111")  # This overrides the value set in your configuration/settings.
cass.set_default_region("NA")


def index():
    # show summoner results once fields are submitted and hide otherwise
    if request.vars.name is None or request.vars.name2 is None:
        show_results = False
    else:
        show_results = True

    all_champions = Champions(region="NA")
    r_val = randint(0, len(all_champions) - 1)
    champ = all_champions[r_val]
    skins = champ.skins
    r_val2= randint(0, len(skins) - 1)
    random_skin = skins[r_val2]

    loading = False

    if show_results:
        region_selected = request.vars.reg  # user input for region selection
        summoner_name = request.vars.name   # user input for summoner 1
        summoner_name2 = request.vars.name2 # user input for summoner 2

        if request.vars.champs is None:
            champion_name = "Ahri"  # default selection (can be any champion)
        else:
            champion_name = request.vars.champs

        try:
            summoner = Summoner(name=str(summoner_name), region=region_selected)
            summoner2 = Summoner(name=str(summoner_name2), region=region_selected)

            if (summoner.exists == False or summoner2.exists == False):
                redirect(URL('default', 'index'))

            all_champions = Champions(region=region_selected)
            champ = all_champions[champion_name]
            r_val3 = randint(0, len(champ.skins) - 1)
            r_val4 = randint(0, len(champ.skins) - 1)

            mh_playing_champ = summoner.match_history.filter(lambda mh: mh.participants[summoner].champion == champ)
            mh_playing_champ2 = summoner2.match_history.filter(lambda mh: mh.participants[summoner2].champion == champ)
            mh_len = len(mh_playing_champ)
            mh_len2 = len(mh_playing_champ2)

            matches_blue_team = [1, 2, 3, 4, 5]
            matches_red_team = [1, 2, 3, 4, 5]
            matches_blue_team2 = [1, 2, 3, 4, 5]
            matches_red_team2 = [1, 2, 3, 4, 5]

            matches_sum = [0] * mh_len
            matches_sum2 = [0] * mh_len2

            sum_wins = 0
            sum_wins2 = 0
            sum_average_kills = 0
            sum_average_kills2 = 0
            sum_average_deaths = 0
            sum_average_deaths2 = 0
            sum_average_assists = 0
            sum_average_assists2 = 0
            sum_average_damage = 0
            sum_average_damage2 = 0
            sum_average_minions = 0
            sum_average_minions2 = 0
            sum_average_vision = 0
            sum_average_vision2 = 0
            last_frame_index = 0
            latest_frame = 0


            insufficient_info = False
            if mh_len > 9:
                index = 0
                while index < mh_len-1:
                    if mh_playing_champ[index].participants[summoner].stats.win:
                        sum_wins += 1
                    index += 1
            else:
                insufficient_info = True

            insufficient_info2 = False
            if mh_len2 > 9:
                index = 0
                while index < mh_len2-1:
                    if mh_playing_champ2[index].participants[summoner2].stats.win:
                        sum_wins2 += 1
                    index += 1
            else:
                insufficient_info2 = True

            insufficient_info = False
            if mh_len > 9:
                index = 0
                print("index:" + str(index))
                print("mh_len:" + str(mh_len))
                while index < mh_len-1:
                    matches_sum[index] = mh_playing_champ[index].participants[summoner].stats.kills
                    index += 1
                sum_average_kills = str(round(sum(matches_sum) / mh_len, 1))
            else:
                insufficient_info = True

            insufficient_info2 = False
            if mh_len2 > 9:
                index = 0
                while index < mh_len2-1:
                    matches_sum2[index] = mh_playing_champ2[index].participants[summoner2].stats.kills
                    index += 1
                sum_average_kills2 = str(round(sum(matches_sum2) / mh_len2, 1))
            else:
                insufficient_info2 = True

            insufficient_info = False
            if mh_len > 9:
                index = 0
                while index < mh_len-1:
                    matches_sum[index] = mh_playing_champ[index].participants[summoner].stats.deaths
                    index += 1
                sum_average_deaths = str(round(sum(matches_sum) / mh_len, 1))
            else:
                insufficient_info = True

            insufficient_info2 = False
            if mh_len2 > 9:
                index = 0
                while index < mh_len2-1:
                    matches_sum2[index] = mh_playing_champ2[index].participants[summoner2].stats.deaths
                    index += 1
                sum_average_deaths2 = str(round(sum(matches_sum2) / mh_len2, 1))
            else:
                insufficient_info2 = True

            insufficient_info = False
            if mh_len > 9:
                index = 0
                while index < mh_len-1:
                    matches_sum[index] = mh_playing_champ[index].participants[summoner].stats.assists
                    index += 1
                sum_average_assists = str(round(sum(matches_sum) / mh_len, 1))
            else:
                insufficient_info = True

            insufficient_info2 = False
            if mh_len2 > 9:
                index = 0
                while index < mh_len2-1:
                    matches_sum2[index] = mh_playing_champ2[index].participants[summoner2].stats.assists
                    index += 1
                sum_average_assists2 = str(round(sum(matches_sum2) / mh_len2, 1))
            else:
                insufficient_info2 = True

            insufficient_info = False
            if mh_len > 9:
                index = 0
                while index < mh_len-1:
                    matches_sum[index] = mh_playing_champ[index].participants[summoner].stats.total_damage_dealt_to_champions
                    index += 1
                sum_average_damage = str(int(sum(matches_sum) / mh_len))
            else:
                insufficient_info = True

            insufficient_info2 = False
            if mh_len2 > 9:
                index = 0
                while index < mh_len2-1:
                    matches_sum2[index] = mh_playing_champ2[index].participants[summoner2].stats.total_damage_dealt_to_champions
                    index += 1
                sum_average_damage2 = str(int(sum(matches_sum2) / mh_len2))
            else:
                insufficient_info2 = True

            insufficient_info = False
            if mh_len > 9:
                index = 0
                while index < mh_len-1:
                    matches_sum[index] = (mh_playing_champ[index].participants[summoner].stats.total_minions_killed +
                        mh_playing_champ[index].participants[summoner].stats.neutral_minions_killed)
                    index += 1
                sum_average_minions = str(int(sum(matches_sum) / mh_len))
            else:
                insufficient_info = True

            insufficient_info2 = False
            if mh_len2 > 9:
                index = 0
                while index < mh_len2-1:
                    matches_sum2[index] = (mh_playing_champ2[index].participants[summoner2].stats.total_minions_killed +
                        mh_playing_champ2[index].participants[summoner2].stats.neutral_minions_killed)
                    index += 1
                sum_average_minions2 = str(int(sum(matches_sum2) / mh_len2))
            else:
                insufficient_info2 = True

            insufficient_info = False
            if mh_len > 9:
                index = 0
                while index < mh_len-1:
                    matches_sum[index] = mh_playing_champ[index].participants[summoner].stats.vision_score
                    index += 1
                sum_average_vision = str(round(sum(matches_sum) / mh_len, 2))
            else:
                insufficient_info = True

            insufficient_info2 = False
            if mh_len2 > 9:
                index = 0
                while index < mh_len2-1:
                    matches_sum2[index] = mh_playing_champ2[index].participants[summoner2].stats.vision_score
                    index += 1
                sum_average_vision2 = str(round(sum(matches_sum2) / mh_len2, 2))
            else:
                insufficient_info2 = True

            # index = 0
            # for s in summoner.match_history[0].blue_team.participants:
            #     matches_blue_team[index] = Champion(name=str(s.champion.name))
            #     index += 1
            #
            # index = 0
            # for s in summoner.match_history[0].red_team.participants:
            #     matches_red_team[index] = Champion(name=str(s.champion.name))
            #     index += 1
            # index = 0
            # for s in summoner2.match_history[0].blue_team.participants:
            #     matches_blue_team2[index] = Champion(name=str(s.champion.name))
            #     index += 1
            #
            # index = 0
            # for s in summoner2.match_history[0].red_team.participants:
            #     matches_red_team2[index] = Champion(name=str(s.champion.name))
            #     index += 1

            cm = ChampionMastery(champion=champ, summoner=summoner, region=region_selected)
            try:
                solo_rank = str(summoner.leagues.fives.tier) + " " + str(summoner.leagues.fives.entries[summoner].division)
                pass
            # exception case if solo rank does not exist for summoner 1
            except KeyError:
                solo_rank = "N/A"
                pass
            try:
                flex_rank = str(summoner.leagues.flex.tier) + " " + str(summoner.leagues.flex.entries[summoner].division)
                # exception case if flex rank does not exist for summoner 1
            except KeyError:
                flex_rank = "N/A"
                pass
            cm2 = ChampionMastery(champion=champ, summoner=summoner2, region=region_selected)
            try:
                solo_rank2 = str(summoner2.leagues.fives.tier) + " " + str(summoner2.leagues.fives.entries[summoner2].division)
                pass
            # exception case if solo rank does not exist for summoner 2
            except KeyError:
                solo_rank2 = "N/A"
                pass
            try:
                flex_rank2 = str(summoner2.leagues.flex.tier) + " " + str(summoner2.leagues.flex.entries[summoner2].division)
                # exception case if flex rank does not exist for summoner 2
            except KeyError:
                flex_rank2 = "N/A"
                pass
        # exception case for blank fields for summoner 1 or summoner 2
        except KeyError:
            redirect(URL('default', 'index'))
            pass

        return dict(show_results=show_results, random_skin=random_skin,champ=champ, summoner=summoner, summoner2=summoner2,
            cm=cm, cm2=cm2, solo_rank=solo_rank, solo_rank2=solo_rank2, flex_rank=flex_rank, flex_rank2=flex_rank2,
            matches_blue_team=matches_blue_team, matches_red_team=matches_red_team, matches_blue_team2=matches_blue_team2, matches_red_team2=matches_red_team2,
            sum_average_kills=sum_average_kills, sum_average_kills2=sum_average_kills2,sum_average_deaths=sum_average_deaths, sum_average_deaths2=sum_average_deaths2,
            sum_average_assists=sum_average_assists, sum_average_assists2=sum_average_assists2, sum_average_damage=sum_average_damage, sum_average_damage2=sum_average_damage2,
            sum_average_minions=sum_average_minions, sum_average_minions2= sum_average_minions2, sum_average_vision=sum_average_vision, sum_average_vision2=sum_average_vision2,
            sum_wins=sum_wins, sum_wins2=sum_wins2, insufficient_info=insufficient_info,insufficient_info2=insufficient_info2, mh_len=mh_len, mh_len2=mh_len2, r_val3=r_val3, r_val4=r_val4)
    else:
        return dict(show_results=show_results, random_skin=random_skin)

# <div class="rounded container padded center">
#     <h3>Last Match</h3>
#     <div class="padded quarter">
#     <div>
#       <div class="center">
#       </div>
#       <div class="blue padded">
#           {{if summoner.match_history[0].blue_team.participants[0].stats.win is True:}}
#           <h6>Blue Team (VICTORY)</h6>
#           {{pass}}
#           {{if summoner.match_history[0].blue_team.participants[0].stats.win is not True:}}
#             <h6>Blue Team (DEFEAT)</h6>
#           {{pass}}
#           {{i = -1
#           for sum in summoner.match_history[0].blue_team.participants:
#           i+= 1}}
#                     <h5>
#                         <img src= "{{=matches_blue_team[i].image.url}}" height="40" width="40">
#                         <img src= "{{=sum.summoner_spell_d.image.url}}" height="20" width="20">
#                         <img src= "{{=sum.summoner_spell_f.image.url}}" height="20" width="20">
#                         <img src= "{{=sum.runes.keystone.image.url}}" height="20" width="20">
#                         {{ =sum.summoner.name}}
#                     </h5>
#               <div>KDA: {{=sum.stats.kills}} / {{=sum.stats.deaths}} / {{=sum.stats.assists}}</div>
#               <div>Damage: {{=sum.stats.total_damage_dealt_to_champions}}</div>
#               <div>CS: {{=sum.stats.total_minions_killed + sum.stats.neutral_minions_killed}}</div>
#               <div>Vision Score: {{=sum.stats.vision_score}}</div>
#           {{pass}}
#       </div>
#             <div id="piechart1" style="width: 900px; height: 500px;"></div>
#       <div class="red padded">
#                 {{if summoner.match_history[0].red_team.participants[0].stats.win is True:}}
#             <h6>Red Team (VICTORY)</h6>
#             {{pass}}
#           {{if summoner.match_history[0].red_team.participants[0].stats.win is not True:}}
#             <h6>Red Team (DEFEAT)</h6>
#           {{pass}}
#           {{i = -1
#           for sum in summoner.match_history[0].red_team.participants:
#           i+= 1}}
#                     <h5>
#                         <img src= "{{=matches_red_team[i].image.url}}" height="40" width="40">
#                         <img src= "{{=sum.summoner_spell_d.image.url}}" height="20" width="20">
#                         <img src= "{{=sum.summoner_spell_f.image.url}}" height="20" width="20">
#                         <img src= "{{=sum.runes.keystone.image.url}}" height="20" width="20">
#                         {{ =sum.summoner.name}}
#                     </h5>
#               <div>KDA: {{=sum.stats.kills}} / {{=sum.stats.deaths}} / {{=sum.stats.assists}}</div>
#               <div>Damage: {{=sum.stats.total_damage_dealt_to_champions}}</div>
#                     <div>CS: {{=sum.stats.total_minions_killed + sum.stats.neutral_minions_killed}}</div>
#               <div>Vision Score: {{=sum.stats.vision_score}}</div>
#           {{pass}}
#         </div>
#                 <div id="piechart2" style="width: 900px; height: 500px;"></div>
#         </div>
#         </div>
#
#         <div class="padded quarter">
#         <div>
#             <div class="center">
#         </div>
#         <div class="blue padded">
#             {{if summoner2.match_history[0].blue_team.participants[0].stats.win is True:}}
#                 <h6>Blue Team (VICTORY)</h6>
#             {{pass}}
#             {{if summoner2.match_history[0].blue_team.participants[0].stats.win is not True:}}
#                 <h6>Blue Team (DEFEAT)</h6>
#             {{pass}}
#                     {{i = -1
#             for sum in summoner2.match_history[0].blue_team.participants:
#             i+= 1}}
#                         <h5>
#                             <img src= "{{=matches_blue_team2[i].image.url}}" height="40" width="40">
#                             <img src= "{{=sum.summoner_spell_d.image.url}}" height="20" width="20">
#                             <img src= "{{=sum.summoner_spell_f.image.url}}" height="20" width="20">
#                             <img src= "{{=sum.runes.keystone.image.url}}" height="20" width="20">
#                             {{ =sum.summoner.name}}
#                         </h5>
#               <div>KDA: {{=sum.stats.kills}} / {{=sum.stats.deaths}} / {{=sum.stats.assists}}</div>
#               <div>Damage: {{=sum.stats.total_damage_dealt_to_champions}}</div>
#               <div>CS: {{=sum.stats.total_minions_killed + sum.stats.neutral_minions_killed}}</div>
#               <div>Vision Score: {{=sum.stats.vision_score}}</div>
#             {{pass}}
#         </div>
#                 <div id="piechart3" style="width: 900px; height: 500px;"></div>
#         <div class="red padded">
#             {{if summoner2.match_history[0].red_team.participants[0].stats.win is True:}}
#                 <h6>Red Team (VICTORY)</h6>
#             {{pass}}
#             {{if summoner2.match_history[0].red_team.participants[0].stats.win is not True:}}
#                 <h6>Red Team (DEFEAT)</h6>
#             {{pass}}
#                     {{i = -1
#             for sum in summoner2.match_history[0].red_team.participants:
#             i+= 1}}
#                         <h5>
#                             <img src= "{{=matches_red_team2[i].image.url}}" height="40" width="40">
#                             <img src= "{{=sum.summoner_spell_d.image.url}}" height="20" width="20">
#                             <img src= "{{=sum.summoner_spell_f.image.url}}" height="20" width="20">
#                             <img src= "{{=sum.runes.keystone.image.url}}" height="20" width="20">
#                             {{ =sum.summoner.name}}
#                         </h5>
#             <div>KDA: {{=sum.stats.kills}} / {{=sum.stats.deaths}} / {{=sum.stats.assists}}</div>
#             <div>Damage: {{=sum.stats.total_damage_dealt_to_champions}}</div>
#             <div>CS: {{=sum.stats.total_minions_killed + sum.stats.neutral_minions_killed}}</div>
#             <div>Vision Score: {{=sum.stats.vision_score}}</div>
#             {{pass}}
#         </div>
#                 <div id="piechart4" style="width: 900px; height: 500px;"></div>
#         </div>
#         </div>
#     </div>

# <script type="text/javascript" class = "center" src="https://www.gstatic.com/charts/loader.js"></script>
#
# <script class="center" type="text/javascript">
# // Load google charts
# google.charts.load('current', {'packages':['corechart']});
# google.charts.setOnLoadCallback(drawChart);
#
# // Draw the chart and set the chart values
# function drawChart() {
#     var data = google.visualization.arrayToDataTable([
#             ['Champion', 'Damage',],
#             ['{{=matches_red_team2[0].name}}', {{=summoner2.match_history[0].red_team.participants[0].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_red_team2[1].name}}', {{=summoner2.match_history[0].red_team.participants[1].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_red_team2[2].name}}', {{=summoner2.match_history[0].red_team.participants[2].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_red_team2[3].name}}', {{=summoner2.match_history[0].red_team.participants[3].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_red_team2[4].name}}', {{=summoner2.match_history[0].red_team.participants[4].stats.total_damage_dealt_to_champions}}]
#         ]);
#
#     // Optional; add a title and set the width and height of the chart
#     var options = {'title':'Total Damage Dealt', 'width':550, 'height':400, 'titleColor':'#FFFFFF', 'color':'#FFFFFF', 'backgroundColor': '#000000'};
#
#     // Display the chart inside the <div> element with id="piechart"
#     var chart = new google.visualization.PieChart(document.getElementById('piechart4'));
#     chart.draw(data, options);
# }
# </script>
# <script class="center" type="text/javascript">
# // Load google charts
# google.charts.load('current', {'packages':['corechart']});
# google.charts.setOnLoadCallback(drawChart);
#
# // Draw the chart and set the chart values
# function drawChart() {
#     var data = google.visualization.arrayToDataTable([
#             ['Champion', 'Damage',],
#             ['{{=matches_blue_team2[0].name}}', {{=summoner2.match_history[0].blue_team.participants[0].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_blue_team2[1].name}}', {{=summoner2.match_history[0].blue_team.participants[1].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_blue_team2[2].name}}', {{=summoner2.match_history[0].blue_team.participants[2].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_blue_team2[3].name}}', {{=summoner2.match_history[0].blue_team.participants[3].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_blue_team2[4].name}}', {{=summoner2.match_history[0].blue_team.participants[4].stats.total_damage_dealt_to_champions}}]
#         ]);
#
#     // Optional; add a title and set the width and height of the chart
#     var options = {'title':'Total Damage Dealt', 'width':550, 'height':400, 'titleColor':'#FFFFFF', 'color':'#FFFFFF', 'backgroundColor': '#000000'};
#
#     // Display the chart inside the <div> element with id="piechart"
#     var chart = new google.visualization.PieChart(document.getElementById('piechart3'));
#     chart.draw(data, options);
# }
# </script>
# <script class="center" type="text/javascript">
# // Load google charts
# google.charts.load('current', {'packages':['corechart']});
# google.charts.setOnLoadCallback(drawChart);
#
# // Draw the chart and set the chart values
# function drawChart() {
#     var data = google.visualization.arrayToDataTable([
#             ['Champion', 'Damage',],
#             ['{{=matches_red_team[0].name}}', {{=summoner.match_history[0].red_team.participants[0].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_red_team[1].name}}', {{=summoner.match_history[0].red_team.participants[1].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_red_team[2].name}}', {{=summoner.match_history[0].red_team.participants[2].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_red_team[3].name}}', {{=summoner.match_history[0].red_team.participants[3].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_red_team[4].name}}', {{=summoner.match_history[0].red_team.participants[4].stats.total_damage_dealt_to_champions}}]
#         ]);
#
#     // Optional; add a title and set the width and height of the chart
#     var options = {'title':'Total Damage Dealt', 'width':550, 'height':400, 'titleColor':'#FFFFFF', 'color':'#FFFFFF', 'backgroundColor': '#000000'};
#
#     // Display the chart inside the <div> element with id="piechart"
#     var chart = new google.visualization.PieChart(document.getElementById('piechart2'));
#     chart.draw(data, options);
# }
# </script>
# <script class="center" type="text/javascript">
# // Load google charts
# google.charts.load('current', {'packages':['corechart']});
# google.charts.setOnLoadCallback(drawChart);
#
# // Draw the chart and set the chart values
# function drawChart() {
#     var data = google.visualization.arrayToDataTable([
#             ['Champion', 'Damage',],
#             ['{{=matches_blue_team[0].name}}', {{=summoner.match_history[0].blue_team.participants[0].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_blue_team[1].name}}', {{=summoner.match_history[0].blue_team.participants[1].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_blue_team[2].name}}', {{=summoner.match_history[0].blue_team.participants[2].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_blue_team[3].name}}', {{=summoner.match_history[0].blue_team.participants[3].stats.total_damage_dealt_to_champions}}],
#             ['{{=matches_blue_team[4].name}}', {{=summoner.match_history[0].blue_team.participants[4].stats.total_damage_dealt_to_champions}}]
#         ]);
#
#     // Optional; add a title and set the width and height of the chart
#     var options = {'title':'Total Damage Dealt', 'width':550, 'height':400, 'titleColor':'#FFFFFF', 'color':'#FFFFFF', 'backgroundColor': '#000000'};
#
#     // Display the chart inside the <div> element with id="piechart"
#     var chart = new google.visualization.PieChart(document.getElementById('piechart1'));
#     chart.draw(data, options);
# }
# </script>
