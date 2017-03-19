# ! /bin/python

def indent(elem, level=0):
    i = '\n' + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            

def escape( input ):
	input.replace('<', '&lt;')
	input.replace('>', '&gt;')
	input.replace('=', '&eq;')
	return input
	
def unescape( input ):
	input.replace('&lt;', '<')
	input.replace('&gt;', '>')
	input.replace('&eq;', '=')
	return input