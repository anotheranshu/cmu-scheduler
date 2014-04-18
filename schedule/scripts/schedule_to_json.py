import json
import graph

courses = [[15251, 15213, 15214],[15167],[15872],[18766]]


def getJson(courses):
    result = []
    for year in xrange(len(courses)):
        result += [{"name" : str(year), \
        "children" : [{"name": str(elem), "size": 3938} \
        for elem in courses[year]]}]

    return json.dumps({"name" : "schedule", "children" : result}, \
                      sort_keys=False, indent=4, separators=(',', ': '))

def main():
    print getJson(graph.findUnits())

main()