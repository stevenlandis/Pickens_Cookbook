import os

def printInfo(address):
	options = os.listdir(address)
	for o in options:
		if o != '.DS_Store' and o != 'info.txt':
			i = address+'/'+o
			#print(i)
			source = ''
			if os.path.isdir(i):
				# print('\tThis is a directory')
				# print('\tIt will link to:',fileList(i))
				# print('\tThe formal title:',getFormalName(i))
				# print('\tThe content title:',getFormalName(i))
				# print('\tThe page title:',pageName(o))

				source += '@title\n'+getFormalName(i)
				source += '\n@contentTitle\n'+getFormalName(i)
				source += '\n@body'
				list = fileList(i)
				for l in list:
					source += '\n-link to='+pageName(l)+' '+getFormalName(i+'/'+l)

				if address != './source':
					# print('\tThis will have a navigation bar with title',getFormalName(address))
					# print('\t\t\tThis will link to',pageName(address.split('/')[-1]))
					navLinks = []
					list = fileList(address)
					for l in list:
						navLinks.append([pageName(l), getFormalName(address+'/'+l)])
					# print('\t   ',navLinks)

					source += '\n@navTitle\n'+getFormalName(address)
					source += '\n@navTitleDestination\n'+pageName(address.split('/')[-1])
					source += '\n@navBody'
					for n in navLinks:
						source += '\n'+n[0]+' '+n[1]

				printInfo(i)
			else:
				# print('\tThis is an ordinary file')
				# print('\tThe formal title:',getFormalName(i))
				# print('\tThe page title:',pageName(o))
				# print('\tThe content title:',getAttribute(fileText(i), 'contentTitle'))
				source = fileText(i)

				if getAttribute(source, 'contentTitle') == 'unknown':
					source += '\n@contentTitle\n'+getFormalName(i)

				if address != './source':
					# print('\tThis will have a navigation bar with title',getFormalName(address))
					navLinks = []
					list = fileList(address)
					for l in list:
						navLinks.append([pageName(l), getFormalName(address+'/'+l)])
					# print('\t   ',navLinks)

					source += '\n@navTitle\n'+getFormalName(address)
					source += '\n@navTitleDestination\n'+pageName(address.split('/')[-1])
					source += '\n@navBody'
					for n in navLinks:
						source += '\n'+n[0]+' '+n[1]

				
			#print(source)

			f = open('./html/'+pageName(o), 'w')
			f.truncate()
			f.write(makePage(source, pageName(o)))
			f.close()

def fileText(file):
	f = open(file, 'r')
	txt = f.read()
	f.close()
	return txt

def fileList(directory):
	options  = os.listdir(directory)
	result = []
	for i in options:
		if i != '.DS_Store' and i != 'info.txt':
			result.append(i)
	return result

def pageName(name):
	return name.split('.')[0]+'.html'

def getFormalName(directory):
	if os.path.isdir(directory):
		#finding name of directory
		options = os.listdir(directory)
		for i in options:
			if i == 'info.txt':
				f = open(directory+'/'+i, 'r')
				txt = f.read()
				f.close()
				return getAttribute(fileText(directory+'/'+i), 'title')
		return "Missing info.txt"
	else:
		#finding name of file
		f = open(directory, 'r')
		txt = f.read()
		f.close()
		return getAttribute(txt, 'title')

def getAttribute(txt, name):
	attributeLocation = txt.find('@'+name)
	if attributeLocation == -1:
		return 'unknown'
	startIndex = attributeLocation + len(name) + 1
	while startIndex < len(txt) and (txt[startIndex] == ' ' or txt[startIndex] == '\n'):
		startIndex+=1
	if startIndex == len(txt):
		return 'unknown'

	endIndex = startIndex
	while endIndex < len(txt) and txt[endIndex] != '@':
		endIndex+=1

	while endIndex > startIndex and (txt[endIndex-1] == '\n' or txt[endIndex-1] == ' '):
		endIndex-=1

	if endIndex == startIndex:
		return 'unknown'

	return txt[startIndex:endIndex]

def htmlify(text, navBody = False):
	res = ''
	mode = 'normal'
	for line in text.split('\n'):
		if len(line) == 0:
			continue
		if line[0] == '-':
			command = line[1:].split(' ')[0]
			if command == 'liststart':
				res += '<ol>'
				mode = 'list'
			elif command == 'listend':
				res += '</ol>'
				mode = 'normal'
			elif command == 'img':
				line = line.split(' ')
				width = '300'
				for phrase in line:
					if phrase.find('width=')>-1:
						width = phrase[6:]
				src = line[-1]
				res += '<p class="clipart"><img src="pictures/'+src+'" width="'+width+'px"></p>'
			elif command == 'link':
				line = line.split(' ')
				link = ''
				title = ''
				if line[1].find('to=') >= 0:
					link = line[1][3:]
					title = ' '.join(line[2:])
				else:
					title = ' '.join(line[1:])
					link = title
				res += '<a href="'+link+'"><p>'+title+'</p></a>'
			elif command == 'line':
				res += '<hr>'
			else:
				print("unknown command found:",command)
		else:
			if line[0] == '\t':
				res += '<p class="body-indent">'+line[1:]+'</p>'
			else:
				if mode == 'list':
					res += '<li>'+line+'</li>'
				elif navBody:
					line = line.split(' ')
					res += '<a href="'+line[0]+'"><p>'+" ".join(line[1:])+'</p></a>'
				else:
					res += '<p>'+line+'</p>'
	return res

searchTerms = []
pageDescriptions = []

def makePage(source, address):
	global searchTerms
	global pageDescriptions
	if getAttribute(source, 'navTitle') == 'unknown':
		#normal page
		res = fileText('./templates/normalPage.html')
		res = res.replace('[[title]]', getAttribute(source, 'title'))

		ct = getAttribute(source, 'contentTitle')
		res = res.replace('[[contentTitle]]', ct)
		ct = ct.lower().split(' ')
		searchTerms += list(zip(ct, [len(pageDescriptions)]*len(ct)))

		pageDescriptions.append([getAttribute(source, 'title'), address, len(ct)])

		res = res.replace('[[body]]', htmlify(getAttribute(source, 'body')))
		return res
	else:
		#navigation page
		res = fileText('./templates/navigationPage.html')
		res = res.replace('[[title]]', getAttribute(source, 'title'))

		ct = getAttribute(source, 'contentTitle')
		res = res.replace('[[contentTitle]]', ct)
		ct = ct.lower().split(' ')
		searchTerms += list(zip(ct, [len(pageDescriptions)]*len(ct)))

		pageDescriptions.append([getAttribute(source, 'title'), address, len(ct)])

		res = res.replace('[[body]]', htmlify(getAttribute(source, 'body')))
		res = res.replace('[[navTitle]]', getAttribute(source, 'navTitle'))
		res = res.replace('[[navTitleDestination]]', getAttribute(source, 'navTitleDestination'))
		res = res.replace('[[navBody]]', htmlify(getAttribute(source, 'navBody'), True))
		return res

def formatSearchTerms(terms):
	res = '['
	for i in range(len(terms)):
		if i != 0:
			res += ','
		res += '["'+terms[i][0]+'", '+str(terms[i][1])+']'
	return res + ']'

printInfo("./source")
# print(formatSearchTerms(searchTerms));
#print(str(pageDescriptions))

f = open('./html/search.js', 'w')
f.truncate()
script = fileText('./templates/search.js')
script = script.replace('[[pageDescriptions]]', str(pageDescriptions))
script = script.replace('[[searchTerms]]', formatSearchTerms(searchTerms))
f.write(script)
f.close()

#print(htmlify(getAttribute(fileText('./source/hints.txt'), 'body')))