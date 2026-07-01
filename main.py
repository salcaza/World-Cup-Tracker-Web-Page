import database as db
from football_api import get_team_schedule, print_schedule
from news_api import get_news, print_news
from gemini_api import get_future_insight, get_headlines_summary
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import TeamSelectionForm
import os
import git

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Welcome to the World Cup Tracker')

@app.route("/team_select", methods=['GET', 'POST'])
def team_select():
    form = TeamSelectionForm()
    schedule = None
    if form.validate_on_submit():
        schedule = get_team_schedule(form.team.data)
    return render_template('team_select.html', title='Team_Schedule', form=form, schedule=schedule)


@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/WorldCupTracker/World-Cup-Tracker-Web-Page')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
