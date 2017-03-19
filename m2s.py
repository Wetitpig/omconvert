def m2s( line ):
	import xml.etree.cElementTree as ET # xml process
	from datetime import datetime as DT # convert timestamp
	from omtools import indent as IX, unescape as ESC
	
	format = '%Y-%m-%dT%H:%M:%SZ'
	op = line.split('>')[0] # object type
	if op == '0':
		op = 'node'
	elif op == '1':
		op = 'way'
	elif op == '2':
		op = 'relation'
	else:
		print('Object type not recognised.')
		quit()
	id = line.split('>')[1] # object id
	# check if id is an integer
	if id.isdigit() == 0 and (id.startswith('-') and id[1:].isdigit()) == 0:
		print('ID contains nom-digit characters.')
		quit()
	vi = line.split('>')[2] # object visibility
	if vi == '0':
		vi = 'false'
	elif vi == '1':
		vi = 'true'
	else:
		print('Unknown visibility.')
		quit()
	vr = line.split('>')[3] # object version
	# check if version is integer
	if vr.isdigit() == 0:
		print('Version number contains non-digit characters.')
		quit()
	cs = line.split('>')[4] # changeset
	# check if changeset is integer
	if cs.isdigit() == 0:
		print('Changeset number contains non-digit characters.')
		quit()
	tm = DT.fromtimestamp(int(line.split('>')[5])).strftime(format) # convert timestamp
	ur = line.split('>')[6] # user name
	ud = line.split('>')[7] # user id
	# check if user id is integer
	if ud.isdigit() == 0:
		print('User ID contains non-digit characters.')
		quit()

	# add root attributes to tree
	root = ET.Element(op)
	root.attrib['id'] = id
	root.attrib['version'] = vr
	root.attrib['changeset'] = cs
	root.attrib['timestamp'] = tm
	root.attrib['user'] = ur
	root.attrib['uid'] = ud
	coor = line.split('>')[8]
	
	# actions for node
	if op == 'node':
		la = coor.split('<')[0]
		lo = coor.split('<')[1]
		root.attrib['lat'] = la # node latitude
		root.attrib['lon'] = lo # node longitude

	# actions for way
	elif op == 'way':
		ndcount = len(coor.split('<'))
		for num2 in range(0, ndcount):
			if coor.split('<')[0] == '':
				break
			nd = ET.SubElement(root, 'nd')
			nd.attrib['ref'] = coor.split('<')[num2] # node reference

	# actions for relation
	elif op == 'relation':
		memcount = len(coor.split('<'))
		for num2 in range(0, memcount):
			single = coor.split('<')[num2] # member
			if single.split('=')[0] == '':
				break
			mm = ET.SubElement(root, 'member')
			# member type
			if single.split('=')[0] == '0':
				tp = 'node'
			if single.split('=')[0] == '1':
				tp = 'way'
			if single.split('=')[0] == '2':
				tp = 'relation'
			nd = single.split('=')[1] # member id
			rl = single.split('=')[2] # member role
			rl = ESC(rl)
			mm.attrib['type'] = tp
			mm.attrib['ref'] = nd
			mm.attrib['role'] = rl

	taglist = line.split('>')[9] # tag list
	tagcount = len(taglist.split('<'))
	for num3 in range(0, tagcount):
		tags = taglist.split('<')[num3]
		if tags.split('=')[0] == '\n':
			break
		tg = ET.SubElement(root, 'tag')
		tk = tags.split('=')[0]
		tv = tags.split('=')[1]
		tk = ESC(tk)
		tv = ESC(tv)
		tg.attrib['k'] = tk # tag key
		tg.attrib['v'] = tv # tag value
			
	IX(root)
			
	# write
	stringoutput = ET.tostring(root, encoding='utf-8', method='xml')
	return stringoutput


def endlast( value, out='' ):
	if value == 3:
		out = '\n</create>'
	elif value == 4:
		out = '\n</modify>'
	elif value == 5:
		out = b'\n</delete>'
	return out

def omc2osc( inputfile, outputfile ):
	import xml.etree.cElementTree as ET # xml process
	import os # check if file is empty
	from time import time as T # timer
	
	# start timer
	start = T()
	input = open(inputfile, 'r')
	
	# create file if not exists
	try:
		tempfile = open(outputfile, 'r')
	except FileNotFoundError:
		tempfile = open(outputfile, 'w')
		tempfile.write('')
		tempfile.close()
		
	# create root for xml
	output = open(outputfile, 'ab+')
	if os.stat(outputfile).st_size == 0:
		temproot = ET.Element('osmChange')
		temproot.attrib['version'] = '0.6'
		temproot.attrib['generator'] = 'omconvert 0.1'
		treetemp = ET.ElementTree(temproot)
		treetemp.write(outputfile, method='xml', short_empty_elements=False)
		output.write(b'\n')
	output.seek(-13, 2)
	output.truncate()
	
	# parse xml
	input = open(inputfile, 'r')
	mfindex = [ ]
	mfindex.append('')
	mfindex.append('')
	
	for line in input:
		# determine modification action
		if line.find('3: ') != -1:
			mfindex[1] = 3
			output.write(endlast(mfindex[0]).encode('utf-8'))
			mfindex[0] = mfindex[1]
			output.write(b'\n<create>\n')
		elif line.find('4: ') != -1:
			mfindex[1] = 4
			output.write(endlast(mfindex[0]).encode('utf-8'))
			mfindex[0] = mfindex[1]
			output.write(b'\n<modify>\n')
		elif line.find('5: ') != -1:
			mfindex[1] = 5
			output.write(endlast(mfindex[0]).encode('utf-8'))
			mfindex[0] = mfindex[1]
			output.write(b'\n<delete>\n')
		else:
			stringoutput = m2s(line)
			output.write(stringoutput.replace(b'&#10;"', b'"'))
	
	if mfindex[0] == 3:
		output.write(b'</create>')
	if mfindex[0] == 4:
		output.write(b'</modify>')
	if mfindex[0] == 5:
		output.write(b'</modify>')
	output.write(b'\n</osmChange>')
	output.close()
	print('Elapsed Time: ' + str(T() - start) + 's')


def omm2osm( inputfile, outputfile ):
	import xml.etree.cElementTree as ET # for xml
	import os # for detecting if file is empty
	from time import time as T # for elapsed time

	# start timer
	start = T()
	
	#create output file if not exists
	try:
		tempfile = open(outputfile, 'r')
	except FileNotFoundError:
		tempfile = open(outputfile, 'w')
		tempfile.write('')
		tempfile.close()
	
	#create root xml root if not exists
	output = open(outputfile, 'ab+')
	if os.path.getsize(outputfile) == 0:
		temproot = ET.Element('osm')
		temproot.attrib['version'] = '0.6'
		temproot.attrib['generator'] = 'omconvert 0.1'
		temproot.attrib['copyright'] = 'OpenStreetMap and contributors'
		temproot.attrib['attribution'] = 'http://www.openstreetmap.org/copyright'
		temproot.attrib['license'] = 'http://opendatacommons.org/licenses/odbl/1-0/'
		temptree = ET.ElementTree(temproot)
		temptree.write(outputfile, encoding='utf-8', method='xml', short_empty_elements=False)
		output.write(b'\n')
	output.seek(-7, 2)
	output.truncate()
	
	input = open(inputfile, 'r')
	for line in input:
		stringoutput = m2s(line)
		if line.split('>')[0] == '0':
			stringoutput = b'\n' + stringoutput + b'\n'
		elif line.split('>')[0] == '2':
			stringoutput = stringoutput[:-1]
		output.write(stringoutput.replace(b'&#10;"', b'"'))
	
	output.write(b'\n</osm>')
	output.close()
	print('Elapsed Time: ' + str(T() - start) + 's')