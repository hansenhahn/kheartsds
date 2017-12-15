
import os

for x in os.listdir('xx'):
	a = open(os.path.join('xx', x), 'r')
	c = a.read().decode('latin-1').encode('utf-8')
	a.close()

	a = open(os.path.join('xx', x), 'w')
	a.write(c)
	a.close()