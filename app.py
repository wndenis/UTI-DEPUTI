from flask import Flask, render_template, url_for, request, redirect
from prepare_data import moves, male_vs_female, total_sums_by_year, calc_region
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/lesser_salary', methods=['GET', 'POST'])
def salary():
    return render_template('lesser_salary.html', years=total_sums_by_year[0], sums=total_sums_by_year[1])

@app.route('/region/<int:id>', methods=['GET', 'POST'])
def region(id):
    return render_template('region.html', region=calc_region(int(id)))

if __name__ == "__main__":
    app.run(debug=True)

# средниее по региону
# пенсия
# вид дохода - есть айди (ключи айди - значение сумма всех доходов в этом (ОБЪЕКТ (incomes) кждый элемент - вид дохода))
# для каждого региона
#    для каждого чиновника 
#       хэш табл массив сумм полученный 

# f(x) -> {income_type1: [income1, income2, ...], income_type2:[income1, income2]}