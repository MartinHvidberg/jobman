
" Don't use yaml, before it become part of default lib

import yaml

with open("../src/jobman_pilot.yaml", 'r') as fil:
    try:
        data = yaml.load(fil)
        print str(type(data)), data
        for k in data.keys():
            print "#", k, ":", str(data[k])
    except yaml.YAMLError as exc:
        print(exc)

