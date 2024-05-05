import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from prettytable import PrettyTable




from robotevents import get_excellence

# Initializes your app with your bot token using socket mode

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# To learn available listener method arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("excellence")
def message_hello(message, say):
    print("Excellence SENT")
    # say() sends a message to the channel where the event was triggered
    teams, drivers_score, prog_score, passing_progs, passing_combined, passing_ranks, ranked_order = get_excellence()

    msg = "Teams Eligible for excellence: \n"#```\n"+repr(table)+"```\n"
    msg += '```\n'
    msg += "Team    Dri  Prg  Com  Rank\n"
    for team in teams:
        d, p = drivers_score[team], prog_score[team]  
        c = d + p
        rank = list(map(lambda x : x[0], ranked_order)).index(team)+1
        msg += f"{team:6}  {d:3}  {p:3}  {c:3}  {rank:2}\n"


    msg += '```\n'

    prog_rank = passing_progs.index('RIT')+1
    overall_rank = passing_ranks.index('RIT')+1
    combined_rank = passing_combined.index('RIT')+1
    msg += f'Programming Skills Rank: {prog_rank}\n'
    msg += f'Combined Skills Rank: {combined_rank}\n'
    msg += f'Overall Rank: {overall_rank}\n'
    say(
        text=msg,
    )


# Start your app
if __name__ == "__main__":
    # start socket mode
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
