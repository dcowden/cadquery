import collections
import re


def try_float(s):
    "Convert to integer if possible."
    try: return float(s)
    except: return s

def natsort_key(s):
	"Used internally to get a tuple by which s is sorted."

	#k = map(try_float, re.findall(r'(\d+|\D+)', s))
	k = map(try_float, re.findall(r'(\d+\.\d+|\d+|\D+ )',s))
	#print k
	return k

def natcmp(a, b):
    "Natural string comparison, case sensitive."
    return cmp(natsort_key(a), natsort_key(b))

def natcasecmp(a, b):
    "Natural string comparison, ignores case."
    return natcmp(a.lower(), b.lower())

def natsort(seq, cmp=natcmp):
    "In-place natural string sort."
    seq.sort(cmp)

def natsorted(seq, cmp=natcmp):
    "Returns a copy of seq, sorted by natural string sort."
    import copy
    temp = copy.copy(seq)
    natsort(temp, cmp)
    return temp

def prettyPrintMap(d,depth=1,indent=1,indentChar='\t',compactLeaf=True,sortFunc=None):
	"""
		prints a lookup table with sane formatting,
		and preserving order.
		FS preserves the key order for dicts, but python doesnt
		we can use collections.OrderedDict to solve that,
		but then pprint or str(dict) doesnt work right
		so we're on on own

		special hack: the last level of the tree is printed all
		onto one line
	"""

	def isLeaf(d):
		for v in d.values():
			if hasattr(v,'__iter__'):
				return False
		return True

	compactOutput = ( isLeaf(d) and compactLeaf )


	first = True

	if compactOutput:
		PAD = ''
		text = ["{" ]
		NEXTENTRY = ""
		ENDPAD = ""
	else:
		PAD = depth * indent * indentChar
		text = ["{\n"]
		NEXTENTRY = "\n"

		if depth > 1:
			ENDPAD = (depth-1) * indent * indentChar
		else:
			ENDPAD = ""

	keys = d.keys()
	if sortFunc != None:
		keys = sortFunc(keys)

	for k in keys:
		if first:
			first = False
		else:
			text.append("," + NEXTENTRY)
		try:
			text.append(PAD + "'" +  str(k) + "': " )
		except:
			log.warn( "Couldnt handle value=",k)
			text.append(PAD + "'WHACKED': " )
		if type(d[k]) == dict or type(d[k]) == collections.OrderedDict:
			text.append( prettyPrintMap(d[k],depth+1,sortFunc=sortFunc ))
		elif type(d[k]) == float or type(d[k]) == int :
			text.append(str(d[k]))
		else:
			text.append("'" + str(d[k]) + "'")
	text.append(NEXTENTRY + ENDPAD + "}")
	return ''.join(text)

if __name__ == '__main__':
	print natsorted([ 'W 45 X 0.1034 ' , 'W 45 X 0.501', 'W 45 X 0.107' ])
