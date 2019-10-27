from prepare_data import calc_region


def quick_sort(arr, low, high): 
    return sorted(arr)

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
                if prop["square"]:
                    estates[prop_type].append(prop["square"])
    return estates

def med_region_real_estate(id):
    estates = region_real_estate(id)
    med_estates = {}

    for prop_type in estates:
        arr = estates[prop_type]
        n = len(arr)
        arr = sorted(arr)

        if n == 1:
            res = arr[0]
        elif n % 2 == 0:
            mid = n // 2
            res = (arr[mid] + arr[mid - 1]) / 2
        else:
            mid = n // 2
            res = arr[mid]
        
        med_estates[prop_type] = res
    
    return med_estates
