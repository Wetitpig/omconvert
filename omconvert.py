# ! /bin/python

import sys
#for sys.argv
from s2m import osm2omm as MM, osc2omc as MC
from m2s import omm2osm as SM, omc2osc as SC

#Check if valid number of arguments.
if len(sys.argv) != 3:
	print('Invalid number of arguments.')
	print('First argument for input file name.')
	print('Second argument for output file name.')

#Direct to different functions.
if sys.argv[1].find('.osm') != -1 and sys.argv[2].find('.omm') != -1:
	MM(sys.argv[1], sys.argv[2])
elif sys.argv[1].find('.omm') != -1 and sys.argv[2].find('.osm') != -1:
	SM(sys.argv[1], sys.argv[2])
elif sys.argv[1].find('.osc') != -1 and sys.argv[2].find('.omc') != -1:
	MC(sys.argv[1], sys.argv[2])
elif sys.argv[1].find('.omc') != -1 and sys.argv[2].find('.osc') != -1:
	SC(sys.argv[1], sys.argv[2])
else:
	print('Invalid file type or file extension.')
	print('Input: .osm or .omm (OSM), or .osc or .omc(OSM Change)')
	print('Output: .osm or .omm (OSM), or .osc or .omc(OSM Change)')
	print('Currently reading from standard input or printing to standard output is not supported.')