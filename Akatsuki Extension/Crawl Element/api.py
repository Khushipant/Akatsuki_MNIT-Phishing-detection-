from flask import Flask, render_template, request
from crawltestsemi import Cubdo # Import your existing script

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        if date:
            cubdo = Cubdo(tgl=date, out="output.txt")
            cubdo.gasken()
            return "Data scraped and saved to domain_log.txt"
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)
