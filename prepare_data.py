import json
import os.path
from datetime import datetime, date, time


# with open("../declarations_sample.json", "r") as f:
with open("static/json/dec.json", "r", encoding="utf-8") as f:
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
    # print(stats.items())
    stats2 = sorted(list(stats.items()), key=lambda x: x[0])
    return stats2

    # Print for debug
    for year, sum in stats.items():
        print(f"=== {year} ===")
        print(f"{year} \t {sum}")

# Return only people's ids of specific region
def calc_region_ids(idToSearch):
    if (not os.path.exists('static/json/region.json')):
        make_region_file()
    with open("static/json/region.json", "r", encoding="utf-8") as f:
        regions = json.load(f)
    idToSearch = str(idToSearch)
    result = list()
    if idToSearch in regions.keys():
        for elem in regions[idToSearch]:
            if checkPersonId(elem):
                result.append(elem['main']['person']['id'])
    return result

# Calculate all incomes based on region (only relative null)
def calc_sum_region(idToSearch):
    if (not os.path.exists('static/json/region.json')):
        make_region_file()
    with open("static/json/region.json", "r", encoding="utf-8") as f:
        regions = json.load(f)
    totalIncomes = []
    idToSearch = str(idToSearch)
    if (idToSearch in regions.keys()):
        for elem in regions[idToSearch]:
            if 'incomes' in elem:
                income = 0
                for item in elem['incomes']:
                    if (not item['relative']):
                        income += item['size']
                totalIncomes.append(income)
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

def calc_migration(id):
    moves = calc_moves()
    from_places = []
    for origin, occurances in moves[id].items():
        from_places.append({"id": origin, "count": occurances})
    sorted_from = sorted(from_places, key=lambda kv: kv["count"], reverse=True)

    i = 0
    res_from = []
    for origin in sorted_from:
        res_from.append(origin["id"])
        i += 1
        if i == 3:
            break
    
    i = 0
    popular_dest = 0
    popular_dest_max = 0
    for dest, origin in moves.items():
        if id in origin and origin[id] > popular_dest_max:
            popular_dest_max = origin[id]
            popular_dest = dest

    return {"top_from": res_from, "top_to": popular_dest}


# Create static/json/region.json file
def make_region_file():
    result = dict()
    for elem in data:
        if 'main' in elem:
            # check if it's a valid year
            if 'year' in elem['main']:
                todayYear = datetime.now().year - 2
                if (elem['main']['year'] >= todayYear):
                    if checkIfRegionExist(elem):
                        regionId = elem['main']['office']['region']['id']
                        if regionId not in result.keys():
                            result[regionId] = [elem]
                        else:
                            result[regionId].append(elem)
    with open("static/json/region.json", "w") as f:
        json.dump(result, f)

# If field 'main''office''region''if' exist - True
def checkIfRegionExist(elem):
    if 'office' in elem['main']:
        if 'region' in elem['main']['office']:
            if elem['main']['office']['region']:
                return True
    return False

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

# Calc medians of female/male incomes of a specific region
# return dict('M': income, 'F': income). Default values - 0
def calc_region_income_gender(idToSearch):
    if (not os.path.exists('static/json/region.json')):
        make_region_file()
    with open("static/json/region.json", "r", encoding="utf-8") as f:
        regions = json.load(f)
    medianIncomes = dict()
    idToSearch = str(idToSearch)
    if (idToSearch in regions.keys()):
        for elem in regions[idToSearch]:
            if checkGender(elem) and checkPersonId(elem):
                gender = elem['main']['person']['gender']
                if gender in medianIncomes.keys():
                    medianIncomes[gender].append(calcAllIncomes(elem))
                else:
                    medianIncomes[gender] = [calcAllIncomes(elem)]
    # print("--------------------- DEBUG --------------------- ")
    # print(medianIncomes)
    # print("--------------------- DEBUG --------------------- ")
    medianIncomes['M'].sort()
    medianIncomes['F'].sort()
    if len(medianIncomes['M']) == 1:
        medianIncomes['M'] = medianIncomes['M'][0]
    if len(medianIncomes['F']) == 1:
        medianIncomes['F'] = medianIncomes['F'][0]
    if len(medianIncomes['M']) % 2 == 0:
        index = len(medianIncomes['M']) // 2
        medianIncomes['M'] = (medianIncomes['M'][index] + medianIncomes['M'][index - 1]) / 2
    else:
        index = len(medianIncomes['M']) // 2
        medianIncomes['M'] = medianIncomes['M'][index]
    if len(medianIncomes['F']) % 2 == 0:
        index = len(medianIncomes['F']) // 2
        medianIncomes['F'] = (medianIncomes['F'][index] + medianIncomes['F'][index - 1]) / 2
    else:
        index = len(medianIncomes['F']) // 2
        medianIncomes['F'] = medianIncomes['F'][index]
    return medianIncomes
    
# True if gender exist
def checkGender(elem):
    if 'main' in elem:
        if 'person' in elem['main']:
            if 'gender' in elem['main']['person']:
                return True
    return False

# True if id exist
def checkPersonId(elem):
    if 'main' in elem:
        if 'person' in elem['main']:
            if 'id' in elem['main']['person']:
                return True
    return False

# Sum all incomes about human (only not relative)
def calcAllIncomes(elem):
    if 'incomes' in elem:
        income = 0
        for item in elem['incomes']:
            if (not item['relative']):
                income += item['size']
        return income
    return 0

# Return dict with keys 'M', 'F' and values - Man's and Women's ids
# in specific region
def calc_region_gender_ids(idToSearch):
    if (not os.path.exists('static/json/region.json')):
        make_region_file()
    with open("static/json/region.json", "r", encoding="utf-8") as f:
        regions = json.load(f)
    people = dict()
    idToSearch = str(idToSearch)
    if (idToSearch in regions.keys()):
        for elem in regions[idToSearch]:
            if checkGender(elem) and checkPersonId(elem):
                gender = elem['main']['person']['gender']
                if gender in people.keys():
                    people[gender].append(elem['main']['person']['id'])
                else:
                    people[gender] = [elem['main']['person']['id']]
    if ('M' not in people.keys()):
        people['M'] = []
    if ('F' not in people.keys()):
        people['F'] = []
    return people

# return Median nubmer of real estates
# by default its 0
def calc_region_median_real_estates(idToSearch):
    if (not os.path.exists('static/json/region.json')):
        make_region_file()
    with open("static/json/region.json", "r", encoding="utf-8") as f:
        regions = json.load(f)
    median = []
    idToSearch = str(idToSearch)
    if (idToSearch in regions.keys()):
        for elem in regions[idToSearch]:
            if 'real_estates' in elem:
                median.append(len(elem['real_estates']))
    median.sort()
    if (len(median) == 0):
        return 0

    if (len(median) == 1):
        return median[0]

    if len(median) % 2 == 0:
        index = len(median) // 2
    else:
        index = len(median) // 2
        return median[index]

# return Median nubmer of vehicle
# by default its 0
def calc_region_median_vehicle(idToSearch):
    if (not os.path.exists('static/json/region.json')):
        make_region_file()
    with open("static/json/region.json", "r", encoding="utf-8") as f:
        regions = json.load(f)
    median = []
    idToSearch = str(idToSearch)
    if (idToSearch in regions.keys()):
        for elem in regions[idToSearch]:
            if 'vehicles' in elem:
                median.append(len(elem['vehicles']))
    median.sort()
    if (len(median) == 0):
        return 0

    if (len(median) == 1):
        return median[0]

    if len(median) % 2 == 0:
        index = len(median) // 2
    else:
        index = len(median) // 2
        return median[index]

# get the most rich person in region
def find_most_rich_region(idToSearch):
    if (not os.path.exists('static/json/region.json')):
        make_region_file()
    with open("static/json/region.json", "r", encoding="utf-8") as f:
        regions = json.load(f)
    mostRich = None
    idToSearch = str(idToSearch)
    if (idToSearch in regions.keys()):
        for elem in regions[idToSearch]:
            income = calcAllIncomes(elem)
            if mostRich is None:
                mostRich = elem
            elif calcAllIncomes(mostRich) < income:
                mostRich = elem
    return mostRich


male_vs_female = calc_disbalance()
total_sums_by_year = calc_sum()
moves = calc_moves()

# with open("static/json/disbalance.json", "w") as f:
#     json.dump(calc_disbalance(), f)

# with open("static/json/sum.json", "w") as f:
#     json.dump(calc_sum(), f)

# with open("static/json/moves.json", "w") as f:
#     json.dump(calc_moves(), f)