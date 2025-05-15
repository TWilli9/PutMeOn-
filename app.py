from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Song Suggestions').sheet1  # or use .worksheet('Sheet1') if needed

@app.route('/', methods=['GET', 'POST'])
def submit_song():
    if request.method == 'POST':
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        song_name = request.form['song_name']
        artist = request.form['artist']
        link = request.form['link']
        submitter = request.form['submitter']

        sheet.append_row([timestamp, song_name, artist, link, submitter])
        return redirect('/thankyou')
    return render_template('form.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
