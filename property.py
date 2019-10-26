from prepare_data import calc_region

def region_real_estate(id):
    declarations = calc_region(id)

    estates = {}
    for dec in declarations:
        for prop in dec["real_estates"]:
            # check if property is completely owned by the official
            if not prop["relative"] and prop["own_type"]["id"] == 20:
                prop_type = prop["type"]["id"]
                if not prop_type in estates:
                    estates[prop_type] = []
                estates[prop_type].append(prop["square"])
    return estates

print("hi")
print(region_real_estate(450))