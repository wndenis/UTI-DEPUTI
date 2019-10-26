from flask import Flask, render_template, url_for, request, redirect
from prepare_data import moves, male_vs_female, total_sums_by_year
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/lesser_salary', methods=['GET', 'POST'])
def salary():
    return render_template('lesser_salary.html', sums=total_sums_by_year)


if __name__ == "__main__":
    app.run(debug=True)

