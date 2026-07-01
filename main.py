import database as db
from football_api import get_team_schedule, print_schedule
from news_api import get_news, print_news
from gemini_api import get_future_insight, get_headlines_summary
from flask import Flask, render_template, url_for, flash, redirect
from forms import TeamSelectionForm
import os

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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
