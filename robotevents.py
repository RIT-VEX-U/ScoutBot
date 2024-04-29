# -*- coding: utf-8 -*-
"""Copy of Meowza.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rB_XHzAF0-L3xk_szm5tIBACgmwmcbdH

# Worlds Analyzer

- Top 30% in prog skills
- Top 30% in combined skills
- Top 30% in rankins per div (30% of both count)
- Won excellence or design at world's qualling event
"""

import requests
import os

apikey =  os.environ.get("ROBOT_EVENTS_TOKEN")

#event_code = 49727
event_code = 53692

def make_request(url: str):
  return requests.get(url, headers = {"Authorization": "Bearer "+apikey}).json()['data']

def get_prog_skills():
  return make_request(f"https://www.robotevents.com/api/v2/events/{event_code}/skills?type%5B%5D=programming&per_page=250")
def get_driver_skills():
  return make_request(f"https://www.robotevents.com/api/v2/events/{event_code}/skills?type%5B%5D=driver&per_page=250")

def get_rankings(div_num):
  return make_request(f"https://www.robotevents.com/api/v2/events/{event_code}/divisions/{div_num}/rankings?&per_page=250")


def top_30_percent(iter):
  l = list(iter)
  end = min(len(l), int(114*.3))
  return l[:end]
  
"""## Data Collection

"""
def get_excellence():
    progs_raw = get_prog_skills()
    drivers_raw = get_driver_skills()

    ranks1 = get_rankings(1)
    ranks2 = get_rankings(2)


    drivers_score = {}
    for elem in drivers_raw:
      drivers_score[elem['team']['name']] = elem['score']
    prog_score = {}
    for elem in progs_raw:
      prog_score[elem['team']['name']] = elem['score']


    drivers = list(map(lambda elem : (elem['team']['name'], elem['score']), drivers_raw))
    progs = list(map(lambda elem : (elem['team']['name'], elem['score']), progs_raw))

    """## Top 30% of rankings"""

    ranks1_in_order = sorted([(elem['team']['name'], elem['rank']) for elem in ranks1], key = lambda elem : elem[1])
    ranks2_in_order = sorted([(elem['team']['name'], elem['rank']) for elem in ranks2], key = lambda elem : elem[1])

    passing_ranks = list(map(lambda x : x[0], top_30_percent(ranks1_in_order) + top_30_percent(ranks2_in_order)))

    """## Top 30% of prog skills"""

    progs_in_order = map(lambda x : x[0], sorted(progs, key = lambda x : x[1], reverse=True))

    passing_progs = top_30_percent(progs_in_order)

    """
    ## Top 30% combined skills"""

    scores = {}
    for elem in drivers:
      if elem[0] in scores:
        scores[elem[0]] += elem[1]
      else:
        scores[elem[0]] = elem[1]
    for elem in progs:
      if elem[0] in scores:
        scores[elem[0]] += elem[1]
      else:
        scores[elem[0]] = elem[1]
    combined =sorted(list(scores.items()), key = lambda x : x[1], reverse = True)

    passing_combined = top_30_percent(map(lambda x : x[0], combined))

    """## Elligible from qualling events"""

    elligible_from_qualling = "AA1 ATUM AUBIE1 AUI BA2 BLRS BLRS2 CDM1 CPSLO EBRT EMU5 FSU GATR1 HAIL IEST1 IQ1 ITESM1 JACKS KU1 MINES MTSAC2 NJIT PERRY PSAU1 PUC4 PYRO QUEEN RIT SENAV1 SJTU1 SJTU2 TCMG2 TJU2 TMAT1 TNTN UACH1 UCF UCR1 UCSA USST1 UTCHE2 UTCJ2 VCAT VTCRO WHOOP WISCO WLDCT WPI".split(' ')

    """# Final"""

    # print("Combined:")
    # print(passing_combined)

    # print("Progs:")
    # print(passing_progs)

    # print("Rankings:")
    # print(passing_ranks)
    # print(progs)

    elligible = list(set(passing_combined) & set(passing_progs) & set(passing_ranks) & set(elligible_from_qualling))
    elligible = sorted(elligible, key = lambda team : drivers_score[team] + prog_score[team], reverse=True)
    
    # print("Teams who are elligible:")
    # print(elligible)
    return elligible, drivers_score, prog_score, passing_progs, passing_combined, passing_ranks

if __name__=='__main__':
    teams, drivers_score, prog_score, passing_progs, passing_combined, passing_ranks = get_excellence()

    print(passing_combined)
    
    msg = ""
    prog_rank = passing_progs.index('RIT')+1
    combined_rank = passing_combined.index('RIT')+1
    msg = ""
    msg += f"Programming Skills Rank: {prog_rank}\n"
    msg += f"Combined Skills Rank: {combined_rank}\n"
    print(msg)
