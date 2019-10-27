from prepare_data import calc_region

def common_fio(id):
    declarations = calc_region(id)
    if not declarations:
        return None

    surnames = {}
    names = {}
    patrs = {}

    for dec in declarations:
        person = dec["main"]["person"]

        s = person["family_name"]
        n = person["given_name"]
        p = person["patronymic_name"]

        if s in surnames:
            surnames[s] += 1
        else:
            surnames[s] = 1

        if n in names:
            names[n] += 1
        else:
            names[n] = 1
        
        if p in patrs:
            patrs[p] += 1
        else:
            patrs[p] = 1

    max = -1
    for s, count in surnames.items():
        if count > max:
            max = count
            com_s = s
    print("surname", max)
    
    max = -1
    for n, count in names.items():
        if count > max:
            max = count
            com_n = n
    print("name", max)

    max = -1
    for p, count in patrs.items():
        if count > max:
            max = count
            com_p = p
    print("pat", max)

    return f"{com_s} {com_n} {com_p}"