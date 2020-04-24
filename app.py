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
    if k >= 12:
        k = 4
        suffix = "T"

    elif k >= 9:
        k = 3
        suffix = "B"

    elif k >= 6:
        k = 2
        suffix = "M"

    elif k >= 3:
        k = 1
        suffix = "K"



    if k > 0:
        xmedian_income /= 1000 ** k
    xmedian_income = "₽%.1f %s" % (xmedian_income, suffix)

    xsquare = prop.med_region_real_estate(id)

    # temp
    if 4 in xsquare:
        xsquare = xsquare[4]
    else:
        xsquare = list(xsquare.values())[0]

    xsquare = "%.0f" % xsquare

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
    region_sorry = [
    {
        "id": 24,
        "name": "Алтайский край"
    },
    {
        "id": 33,
        "name": "Амурская область"
    },
    {
        "id": 37,
        "name": "Архангельская область"
    },
    {
        "id": 38,
        "name": "Астраханская область"
    },
    {
        "id": 96,
        "name": "Белгородская область"
    },
    {
        "id": 35,
        "name": "Брянская область"
    },
    {
        "id": 36,
        "name": "Владимирская область"
    },
    {
        "id": 41,
        "name": "Волгоградская область"
    },
    {
        "id": 42,
        "name": "Вологодская область"
    },
    {
        "id": 43,
        "name": "Воронежская область"
    },
    {
        "id": 93,
        "name": "Еврейская автономная область"
    },
    {
        "id": 44,
        "name": "Забайкальский край"
    },
    {
        "id": 99,
        "name": "Ивановская область"
    },
    {
        "id": 45,
        "name": "Иркутская область"
    },
    {
        "id": 9,
        "name": "Кабардино-Балкарская Республика"
    },
    {
        "id": 46,
        "name": "Калининградская область"
    },
    {
        "id": 97,
        "name": "Калужская область"
    },
    {
        "id": 48,
        "name": "Камчатский край"
    },
    {
        "id": 11,
        "name": "Карачаево-Черкесская республика"
    },
    {
        "id": 50,
        "name": "Кемеровская область"
    },
    {
        "id": 51,
        "name": "Кировская область"
    },
    {
        "id": 53,
        "name": "Костромская область"
    },
    {
        "id": 27,
        "name": "Краснодарский край"
    },
    {
        "id": 28,
        "name": "Красноярский край"
    },
    {
        "id": 98,
        "name": "Курганская область"
    },
    {
        "id": 55,
        "name": "Курская область"
    },
    {
        "id": 56,
        "name": "Ленинградская область"
    },
    {
        "id": 57,
        "name": "Липецкая область"
    },
    {
        "id": 58,
        "name": "Магаданская область"
    },
    {
        "id": 63,
        "name": "Москва"
    },
    {
        "id": 64,
        "name": "Московская область"
    },
    {
        "id": 65,
        "name": "Мурманская область"
    },
    {
        "id": 102,
        "name": "Ненецкий автономный округ"
    },
    {
        "id": 66,
        "name": "Нижегородская область"
    },
    {
        "id": 67,
        "name": "Новгородская область"
    },
    {
        "id": 68,
        "name": "Новосибирская область"
    },
    {
        "id": 69,
        "name": "Омская область"
    },
    {
        "id": 105,
        "name": "Оренбургская область"
    },
    {
        "id": 70,
        "name": "Орловская область"
    },
    {
        "id": 72,
        "name": "Пензенская область"
    },
    {
        "id": 29,
        "name": "Пермский край"
    },
    {
        "id": 74,
        "name": "Приморский край"
    },
    {
        "id": 75,
        "name": "Псковская область"
    },
    {
        "id": 3,
        "name": "Республика Адыгея"
    },
    {
        "id": 6,
        "name": "Республика Алтай"
    },
    {
        "id": 4,
        "name": "Республика Башкортостан"
    },
    {
        "id": 5,
        "name": "Республика Бурятия"
    },
    {
        "id": 59,
        "name": "Республика Дагестан"
    },
    {
        "id": 8,
        "name": "Республика Ингушетия"
    },
    {
        "id": 47,
        "name": "Республика Калмыкия"
    },
    {
        "id": 12,
        "name": "Республика Карелия"
    },
    {
        "id": 13,
        "name": "Республика Коми"
    },
    {
        "id": 109,
        "name": "Республика Крым*"
    },
    {
        "id": 61,
        "name": "Республика Марий Эл"
    },
    {
        "id": 62,
        "name": "Республика Мордовия"
    },
    {
        "id": 92,
        "name": "Республика Саха (Якутия)"
    },
    {
        "id": 17,
        "name": "Республика Северная Осетия — Алания"
    },
    {
        "id": 18,
        "name": "Республика Татарстан"
    },
    {
        "id": 85,
        "name": "Республика Тува (Тыва)"
    },
    {
        "id": 21,
        "name": "Республика Хакасия"
    },
    {
        "id": 76,
        "name": "Ростовская область"
    },
    {
        "id": 103,
        "name": "Рязанская область"
    },
    {
        "id": 77,
        "name": "Самарская область"
    },
    {
        "id": 1,
        "name": "Санкт-Петербург"
    },
    {
        "id": 79,
        "name": "Саратовская область"
    },
    {
        "id": 94,
        "name": "Сахалинская область"
    },
    {
        "id": 80,
        "name": "Свердловская область"
    },
    {
        "id": 110,
        "name": "Севастополь*"
    },
    {
        "id": 100,
        "name": "Смоленская область"
    },
    {
        "id": 81,
        "name": "Ставропольский край"
    },
    {
        "id": 82,
        "name": "Тамбовская область"
    },
    {
        "id": 101,
        "name": "Тверская область"
    },
    {
        "id": 106,
        "name": "Томская область"
    },
    {
        "id": 84,
        "name": "Тульская область"
    },
    {
        "id": 86,
        "name": "Тюменская область"
    },
    {
        "id": 20,
        "name": "Удмуртская республика"
    },
    {
        "id": 88,
        "name": "Ульяновская область"
    },
    {
        "id": 32,
        "name": "Хабаровский край"
    },
    {
        "id": 108,
        "name": "Ханты-Мансийский автономный округ — Югра"
    },
    {
        "id": 89,
        "name": "Челябинская область"
    },
    {
        "id": 90,
        "name": "Чеченская республика"
    },
    {
        "id": 91,
        "name": "Чувашская республика - Чувашия"
    },
    {
        "id": 95,
        "name": "Чукотский автономный округ"
    },
    {
        "id": 104,
        "name": "Ямало-Ненецкий автономный округ"
    },
    {
        "id": 107,
        "name": "Ярославская область"
    }
]
    xreg = "?"
    for r in region_sorry:
        if r["id"] == id:
            xreg = r["name"]
            break

    xvehicle = prepare_data.calc_region_median_vehicle(id)


    # top_gender
    # top_income
    # top_real
    # top_vehicle



    return render_template('region.html', region_id=id, name=xname, gender=xgender, income=xmedian_income, square=xsquare, photo=link, region_name=xreg, vehicles=xvehicle)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5554)

# средниее по региону
# пенсия
# вид дохода - есть айди (ключи айди - значение сумма всех доходов в этом (ОБЪЕКТ (incomes) кждый элемент - вид дохода))
# для каждого региона
#    для каждого чиновника 
#       хэш табл массив сумм полученный 

# f(x) -> {income_type1: [income1, income2, ...], income_type2:[income1, income2]}