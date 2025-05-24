from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# Load credentials from environment variable
creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open('Song Suggestions').sheet1  

@app.route('/', methods=['GET', 'POST'])
def submit_song():
    if request.method == 'POST':
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        song_name = request.form['song_name']
        artist = request.form['artist']
        description = request.form.get('description', '')
        submitter = request.form['submitter']

        sheet.append_row([timestamp, song_name, artist, description, submitter])
        return redirect('/thankyou')
    return render_template('form.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
