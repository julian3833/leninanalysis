# This Python file uses the following encoding: utf-8from __future__ import divisionfrom includes import tokenizer as tkfrom includes import information_value as ivfrom includes import zipf as zffrom includes import works as wk from includes import utilsfrom includes import preprocessor as preimport nltk                   from nltk.corpus import stopwordsfrom nltk.corpus import wordnet as wnimport wn_analyzer as wnaimport matplotlib     import matplotlib.pyplot as plt           import pylab       def get_a_work(year, number):	works = wk.Works()	works.load_dictionary()	dict_1917 = works.get_year(str(year))	one_work = dict_1917[number]	return one_workdef run_zipf(work):		zipf = zf.Zipf(work['text'], work['name'], run=True)def	run_iv(work,words):	ivp = iv.InformationValue(work['text'], words)		return ivp.information_value(100)	def get_window_size(work, words):	x= iv.InformationValue(work['text'],words)		print str(x.calculate_window_size())	def print_year(year, n = 20, verbose=False):	zipf = utils.from_file('zipf_by_year.json')	for x in zipf:		if x['name'] == year:			resume = x			break			data = utils.load_year_data(year, resume)	wn = utils.from_file('by_year/'+year+'_wn.json')	cant  = len(data['base'])	linea = '---------------------------------------------------------------------------'	print 'A�o: '+year	print 'Cantidad de textos: '+str(cant)	print 'Palabras y vocabulario: '+str(data['zipf_resume']['total_words'])+', '+str(data['zipf_resume']['total_vocab'])	if verbose:		print 'Mas usadas: '+ ','.join(map(str, [u.encode('utf-8') for u in data['zipf_resume']['top_words'][:n]]))		print 'Teoricidad  (iv,zipf,zipf_anual): '+str(round(wn['theory_iv'],3))+' , '+str(round(wn['theory_zipf'],3))+',  '+str(round(wn['zipf_resume']['theory'],3))	print 'Practicidad (iv,zipf,zipf_anual): '+str(round(wn['praxis_iv'],3))+' , '+str(round(wn['praxis_zipf'],3))+',  '+str(round(wn['zipf_resume']['praxis'],3))	print linea				i = 0	while i < cant:		if (data['base'][i]['wid'] != data['iv'][i]['wid']) or (data['base'][i]['wid'] != data['zipf'][i]['wid']):			print 'Error al procesar'			break				print 'Texto '+str(i+1)+': '+data['base'][i]['name']		print 'Palabras y vocabulario: '+str(data['zipf'][i]['total_words'])+', '+str(data['zipf'][i]['total_vocab'])		if verbose:			print 'Mas usadas: '+ ','.join( map( str, [u.encode('utf-8') for u in data['zipf'][i]['top_words'][:n]]))			print 'IV: '+ ','.join(map(str, [u.encode('utf-8') for u in data['iv'][i]['top_words'][:n]]))		print 'Teoricidad  (iv,zipf           ): '+str(round(wn['iv'][i]['theory'],3))+' , '+str(round(wn['zipf'][i]['theory'],3)) 		print 'Practicidad (iv,zipf           ): '+str(round(wn['iv'][i]['praxis'],3))+' , '+str(round(wn['zipf'][i]['praxis'],3))		print linea		i= i+1def print_wn(y1, y2):	print 'A�o ',	print 'P    ',	print 'T    ',	print 'P - T',	print '    Zf P ',	print 'Zf T '	#print 'Zfrt '		x = []	y = []	z = []	w = []				 	for year in range(y1, y2):				year = str(year)		data = utils.from_file('by_year/'+year+'_wn.json')		#{			# praxis_iv,		# theory_iv,		# praxis_zipf,		# theory_zipf,		# zipf, #[{wid,yid,distances,theory, praxis}]		# iv, #[{wid,yid,distances,theory, praxis}]		# zipf_resume, #{distances,theory, praxis}				#}				print year,		print str(data['praxis_iv']*10000)[:5], str(data['theory_iv']*10000)[:5],		print str(data['praxis_iv']*10000 - data['theory_iv']*10000)[:5],		print '    '+str(data['praxis_zipf'])[:5] ,str(data['theory_zipf'])[:5],		print str(data['praxis_zipf'] - data['theory_zipf'])[:5]		#,str(data['zipf_resume']['praxis'])[:5] , str(data['zipf_resume']['theory'])[:5]				w.append(data['theory_iv']*10000)		z.append(data['praxis_iv']*10000)		y.append(data['praxis_iv']*10000 - data['theory_iv']*10000)		x.append(year)			#Aca grafico S segun pos tags	#tags = {'j': 'bo', 'n':'ro', 'd':'mo'}		#pylab.axes([0.1, 0.15, 0.8, 0.75])	pylab.xticks(range(1893,1924),  rotation=90)			pylab.plot(x, y, label='p-t')	pylab.plot(x, z, label='p')	pylab.plot(x, w, label='t')	pylab.legend()	pylab.show()	def print_words_by_year():	zipf = utils.from_file('years_zipf.json')	x= []	y = []	for yea in range(1893, 1924):			for year in zipf:			if int(year['name']) == yea:				x.append(str(year['name']))				y.append(float(year['total_words']))		#return x, y	pylab.xticks(range(1893,1924),  rotation=90)	pylab.plot(x,y, label='words(year)')	pylab.legend()	pylab.show()