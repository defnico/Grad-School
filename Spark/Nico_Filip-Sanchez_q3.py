from __future__ import print_function
from pyspark import SparkContext
import sys

if len(sys.argv) != 4:
    print("Usage: q3.py <frequents_file> <likes_file> <output_file>", file=sys.stderr)
    sys.exit(-1)
sc = SparkContext(appName="q3")

frequents_file = sys.argv[1]
likes_file = sys.argv[2]
output_file = sys.argv[3]

frequents = sc.textFile(frequents_file)
likes = sc.textFile(likes_file)

drinkersToBars = frequents.map(lambda s: s.split(',')).groupByKey()
drinkersToBeers = likes.map(lambda s: s.split(',')).groupByKey()

drinkersToBarsAndBeers = drinkersToBars.leftOuterJoin(drinkersToBeers)


def filterDrinkerNoBeers(kv):
    bars, beers = kv[1]
    return beers is None


drinkersNoBeers = drinkersToBarsAndBeers.filter(filterDrinkerNoBeers)

output = drinkersNoBeers.collect()

of = open(output_file, "w")
of.write('Drinker\n')
for kv in output:
    of.write("{}\n".format(kv[0]))
of.close()
