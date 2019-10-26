import json
import os.path
from datetime import datetime, date, time


# with open("../declarations_sample.json", "r") as f:
with open("declarations_sample2_coding.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Calculate deputies' disbalance in income;
# bigger positive value means man earned more than their spouses in the particular region;
# negative values show that women earned more

def calc_disbalance():
    stats = {}

    for i in range(2006, 2018):
        stats[i] = {} # men's disbalance in salary calcualted as index

    for elem in data:
        
        id = elem["main"]["person"]["id"]
        name = elem["main"]["person"]["name"]
        gender = elem["main"]["person"]["gender"]
        year = elem["main"]["year"]
        
        region_object = elem["main"]["office"]["region"]
        if not region_object:
            continue

        region = region_object["id"]

        personal_income = 0
        spouse_income = 0

        for item in elem["incomes"]:
            if item["relative"] and item["relative"]["id"] == 2:
                spouse_income += item["size"]
            else:
                personal_income += item["size"]
        
        
        disbalance = -1
        if  gender == "M" and personal_income > spouse_income or gender == "F" and personal_income < spouse_income:
            disbalance = 1 # that means spouses get advantage

        if year not in stats:
            stats[year] = {}

        if region not in stats[year]:
            stats[year][region] = disbalance
        else:
            stats[year][region] += disbalance

    return stats

    # Print for debug
    for year in stats.keys():
        print(f"=== {year} ===")
        for region, dom in stats[year].items():
            print(region, dom)


# Calculate the overall sum taxpayers payed the deputies (count only their own income)
def calc_sum():
    stats = {}

    for elem in data:

        year = elem["main"]["year"]

        income = 0

        for item in elem["incomes"]:
            if not item["relative"]:
                income += item["size"]

        if year in stats:
            stats[year] += income
        else:
            stats[year] = income
    print(stats.items())
    stats2 = sorted(list(stats.items()), key=lambda x: x[0])
    return stats2

    # Print for debug
    for year, sum in stats.items():
        print(f"=== {year} ===")
        print(f"{year} \t {sum}")


# Calculate all incomes based on region (only relative null)
def calc_sum_region(idToSearch):
    if (not os.path.exists('static/json/region.json')):
        make_region_file()
    with open("static/json/region.json", "r", encoding="utf-8") as f:
        regions = json.load(f)
    totalIncomes = dict()
    if (int(idToSearch) in regions.keys()):
        for key, elem in regions.items():
            if 'incomes' in elem:
                income = 0
                for item in elem['incomes']:
                    if (not item['relative']):
                        income += item['size']
                if (int(key) not in totalIncomes.keys()):
                    totalIncomes[int(key)] = [income]
                else:
                    totalIncomes[int(key)].append(income)
        return totalIncomes
    else:
        return None

# Calculate moves of certain officials and check if there're any trends
def calc_moves():

    stats = {}
    moves = {} # moves to from

    for elem in data:

        id = elem["main"]["person"]["id"]
        year = elem["main"]["year"]
        region_object = elem["main"]["office"]["region"]
        if not region_object:
            continue

        region = region_object["id"]
        
        if not id in stats:
            stats[id] = {}
        stats[id][year] = region


    for off_id, moveHistory in stats.items():
        for year in range(2007, 2018):
            if year not in moveHistory or year - 1 not in moveHistory:
                continue

            region = moveHistory[year]
            prev_region = moveHistory[year - 1]

            if region != prev_region:
                if not region in moves:
                    moves[region] = {}
                if prev_region in moves[region]:
                    moves[region][prev_region] += 1
                else:
                    moves[region][prev_region] = 1

    return moves

    # Print for debug
    for destination in moves.keys():
        for origin, occurances in moves[destination].items():
            print(f"{destination} <-- {origin}: {occurances}")


def make_region_file():
    result = dict()
    for elem in data:
        if 'main' in elem:
            # check if it's a valid year
            if 'year' in elem['main']:
                todayYear = datetime.now().year
                if (elem['main']['year'] == todayYear - 1 or elem['main']['year'] == todayYear - 2):
                    if 'office' in elem['main']:
                        if 'id' in elem['main']['office']:
                            officeId = int(elem['main']['office']['id'])
                            if (officeId not in result.keys()):
                                result[officeId] = [elem]
                            else:
                                result[officeId].append(elem)
    with open("static/json/region.json", "w") as f:
        json.dump(result, f)


# Calculate all deps in specific regions
def calc_region(id):
    idToSearch = str(id)
    if (not os.path.exists('static/json/region.json')):
        make_region_file()
    with open("static/json/region.json", "r", encoding="utf-8") as f:
        regions = json.load(f)
    if idToSearch in regions.keys():
        return regions[idToSearch]
    else:
        return None

male_vs_female = calc_disbalance()
total_sums_by_year = calc_sum()
moves = calc_moves()

# with open("static/json/disbalance.json", "w") as f:
#     json.dump(calc_disbalance(), f)

# with open("static/json/sum.json", "w") as f:
#     json.dump(calc_sum(), f)

# with open("static/json/moves.json", "w") as f:
#     json.dump(calc_moves(), f)