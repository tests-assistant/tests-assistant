import csv

from cStringIO import StringIO


def instances_to_csv(instances):
    output = StringIO()
    writer = csv.writer(output)
    for instance in instances:
        o = list()
        o.append(instance.run.version)
        o.append(instance.test.title)
        o.append(instance.test.description)
        writer.writerow(o)
    return output
