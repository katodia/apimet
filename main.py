#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
import time, sqlite3, urllib2

id = 1
i = 1001
fin = 50298
url = 'http://www.aemet.es/xml/municipios/localidad_%s.xml'
delay = 1
conn = sqlite3.connect('aemet.db')
cursor = conn.cursor()
query = 'INSERT INTO municipio VALUES (%s, "%s", "%s", "%s");'
log = file('log', 'w+')


while i <= fin:
	cod = str(i)
	if len(cod) < 5:
		cod = '0' + cod
	current_url = url % cod
	try:
		response = urllib2.urlopen(current_url)
		xml = etree.parse(response)
		response.close()
		nombre_municipio = unicode(xml.xpath('//nombre')[0].text)
		nombre_provincia = unicode(xml.xpath('//provincia')[0].text)
		current_query = query % ( str(id), nombre_municipio, nombre_provincia, cod )
		try:
			cursor.execute(current_query)
			conn.commit()
			log.write('Added. %s ' % cod)
		except:
			log.write('Error executing: %s \n' % current_query.encode('utf-8') )
	except urllib2.HTTPError:
		pass
	time.sleep(delay)
	i += 1
	id += 1
log.close()
conn.close()

