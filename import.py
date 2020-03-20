#!/usr/bin/env python

import json
import random
from api.models.trucker import TruckerModel
from api.models.check_in import CheckInModel
from config._abstract import AbstractConfig

AbstractConfig.set_up_db()

if len(TruckerModel.get_owner_truckers()) > 0:
    exit(0)

with open('./resources/trucker_samples.json', 'r') as truckers_json_file:
    truckers_data = json.load(truckers_json_file)
    truckers_list = []
    for trucker in truckers_data:
        truckers_list.append(TruckerModel.create_trucker(trucker))

with open('./resources/check_in_samples.json', 'r') as check_ins_json_file:
    check_ins_data = json.load(check_ins_json_file)
    for check_in in check_ins_data:
        o_lng, o_lat = check_in['origin'].split(', ')
        check_in['origin'] = {
            'lng': o_lng,
            'lat': o_lat
        }

        d_lng, d_lat = check_in['destination'].split(', ')
        check_in['destination'] = {
            'lng': d_lng,
            'lat': d_lat
        }

        trucker = random.choice(truckers_list)
        check_in = CheckInModel.create_check_in(data=check_in, trucker=trucker)

        if random.choice([True, False]):
            CheckInModel.checkout(check_in)
