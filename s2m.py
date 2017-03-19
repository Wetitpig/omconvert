def s2m( elem ):
	import xml.etree.cElementTree as ET # xml processing
	from datetime import datetime as DT # convert timestamp
	from omtools import escape as ESC
	
	format = '%Y-%m-%dT%H:%M:%SZ'
	id = elem.attrib.get('id') # object id
	if elem.attrib.get('visible') == 'false':
		vi = '0'
	else:
		vi = '1'
	# check if object id is integer
	if id.isdigit() == 0:
		print('ID contains non-digit characters.')
		quit()
	vr = elem.attrib.get('version') # object version
	# check if object version is integer
	if vr.isdigit() == 0:
		print('Version number contains non-digit characters.')
		quit()
	cs = elem.attrib.get('changeset') # changeset
	# check if changeset is integer
	if cs.isdigit() == 0:
		print('Changeset number contains non-digit characters.')
		quit()
	tm = str(int(DT.timestamp(DT.strptime(elem.attrib.get('timestamp'), format)))) # convert timestamp
	ur = elem.attrib.get('user') # user name
	ud = elem.attrib.get('uid') # user id
	# check if user id is integer
	if ud.isdigit() == 0:
		print('User ID contains non-digit characters.')
		quit()
	row = id + '>' + vi + '>' + vr + '>' + cs + '>' + tm + '>' + ur + '>' + ud + '>'
			
	# actions for node
	if elem.tag == 'node':
		op = '0'
		num2 = 0
		la = elem.attrib.get('lat') # node latitude
		lo = elem.attrib.get('lon') # node longitude
		row = op + '>' + row + la + '<' + lo + '>'
	
	# actions for way
	elif elem.tag == 'way':
		op = '1'
		num2 = 0
		row = op + '>' + row
		if elem.find('nd') != None:
			while elem[num2].tag == 'nd':
				nd = elem[num2].attrib.get('ref') # individual node
				row += nd + '<'
				num2 += 1
			row = row[:-1] # remove last <
		
	# actions for relation
	elif elem.tag == 'relation':
		op = '2'
		num2 = 0
		row = op + '>' + row
		if elem.find('member') != None:
			while elem[num2].tag == 'member':
				if elem[num2].attrib.get('type') == 'node':
					mt = '0'
				elif elem[num2].attrib.get('type') == 'way':
					mt = '1'
				elif elem[num2].attrib.get('type') == 'relation':
					mt = '2'
				else:
					print('Member type not recognised.')
					quit()
				md = elem[num2].attrib.get('ref') # member id
				mr = elem[num2].attrib.get('role') # member role
				mr = ESC(mr)
				row += mt + '=' + md + '=' + mr + '<' # member entry
				num2 += 1
			row = row[:-1]
	
	else:
		print('Object type not recognised.')
		quit()
	
	row += '>'
	num3 = len(elem.getchildren())
	
	for index in range(num2, num3):
		tk = elem[index].attrib.get('k') # tag key
		tk = ESC(tk)
		tv = elem[index].attrib.get('v') # tag value
		tv = ESC(tv)
		row += tk + '=' + tv + '<'
		index += 1
	
	row = row[:-1] + '\n' # finish row
			
	return row
	

def osc2omc( inputfile, outputfile):
	import xml.etree.cElementTree as ET # xml processing
	from time import time as T # timer
	
	# start timer
	start = T()
	output = open(outputfile, 'a')
	
	# parse xml
	context = ET.iterparse(inputfile, events=("start", "end"))
	context = iter(context)
	event, root = next(context)

	for event, elem in context:
		if event == "start" and ( elem.tag == "create" or elem.tag == "modify" or elem.tag == "delete" ):
			# determine modification action
			if elem.tag == 'create':
				output.write('3: \n')
				root.clear()
				continue
			elif elem.tag == 'modify':
				output.write('4: \n')
				root.clear()
				continue
			elif elem.tag == 'delete':
				output.write('5: \n')
				root.clear()
				continue
			else:
				print('Modification method not identified.')
				quit()
		if event == "end" and ( elem.tag == "node" or elem.tag == "way" or elem.tag == "relation" ):
			# write to file
			output.write(m2s(elem))
			root.clear()
	
	# close file
	output.close()
	print('Elapsed Time: ' + str(T() - start) + 's')
	

def osm2omm( inputfile, outputfile ):
	import xml.etree.cElementTree as ET # xml processing
	from time import time as T # timer

	# start timer
	start = T()
	output = open(outputfile, 'a')

	# parse xml
	context = ET.iterparse(inputfile, events=("start", "end"))
	context = iter(context)
	event, root = next(context)

	for event, elem in context:
		if event == "end" and ( elem.tag == "node" or elem.tag == "way" or elem.tag == "relation" ):
			output.write(s2m(elem))
			root.clear()

	# close file
	output.close()
	print('Elapsed time: ' + str(T() - start) + 's')