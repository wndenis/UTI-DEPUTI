from prepare_data import calc_region
from random import randint

def random_person(reg_id):

    declarations = calc_region(reg_id)
    i = randint(0, len(declarations))

    return declarations[i]

