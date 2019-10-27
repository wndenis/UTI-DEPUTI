from flask import Flask, render_template, url_for, request, redirect
from prepare_data import moves, male_vs_female, total_sums_by_year, calc_region
app = Flask(__name__)
from name import common_fio
import prepare_data
import property as prop
from average_face.extract import extract
from average_face.average import average
import os


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
@app.route('/index.html/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/region/<int:id>/', methods=['GET', 'POST'])
def region(id):
    print("FIO")
    xname = common_fio(id)
    if not xname:
        return render_template('404.html')

    print("GENDERS")
    genders = prepare_data.calc_region_gender_ids(id)
    males = len(genders["M"])
    females = len(genders["F"])
    xgender = "M" if males > females else "F"

    incomes = prepare_data.calc_region_income_gender(id)

    female_income = incomes["F"]
    male_income = incomes["M"]
    xmedian_income = (female_income + male_income) / 2
    k = len(str(int(xmedian_income)))
    # print("MEDIAN: %s\nK: %s" % (xmedian_income, k))
    suffix = ""
    if k > 3:
        k = 1
        suffix = "K"
    if k > 6:
        k = 2
        suffix = "M"
    if k > 9:
        k = 3
        suffix = "B"
    if k > 12:
        k = 4
        suffix = "T"

    if k > 0:
        xmedian_income /= 1000 ** k
    xmedian_income = "%.2f%s" % (xmedian_income, suffix)

    xsquare = prop.med_region_real_estate(id)

    # temp
    xsquare = list(xsquare.values())[0]
    xsquare = f"{xsquare}"

    # ==========
    region_people = calc_region(id)
    region_people = {str(elem["main"]["person"]["id"]) for elem in region_people}
    print(region_people)
    link = f"./static/average_faces/{id}.jpg"
    print(link)
    if not os.path.isfile(link):
        link = f"average_faces/{id}.jpg"
        extract()
        photo = average(region_people, id)
        print(photo)
        if not photo:
            link = "default_profile_photo.png"
    else:
        link = f"average_faces/{id}.jpg"
    print(link)
    # make photo


    return render_template('region.html', region_id=id, name=xname, gender=xgender, income=xmedian_income, square=xsquare, photo=link)

if __name__ == "__main__":
    app.run(debug=True)

# средниее по региону
# пенсия
# вид дохода - есть айди (ключи айди - значение сумма всех доходов в этом (ОБЪЕКТ (incomes) кждый элемент - вид дохода))
# для каждого региона
#    для каждого чиновника 
#       хэш табл массив сумм полученный 

# f(x) -> {income_type1: [income1, income2, ...], income_type2:[income1, income2]}