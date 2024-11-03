#!/usr/bin/python3
import sys, subprocess

svg = 'cards.svg'

pw = subprocess.Popen(['inkscape', '-W', svg], stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
ph = subprocess.Popen(['inkscape', '-H', svg], stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)

pw.wait()
ph.wait()

w = float(pw.stdout.read()) / 14
h = float(ph.stdout.read()) / 8

rows = [ 'blue', 'green', 'yellow', 'red' ]
cols = [ str(x) for x in range(0,10) ] + [ 'skip', 'flip', 'draw2' ]

names = []
jobs = []		

def extract(x, y, name):
	global names, jobs
	names.append(name)
	command = [
		'inkscape',
		'--export-dpi=100',
		'--export-png=' + name + '.png',
		'--export-area=' + str(x*w) + ':' + str(y*h) + ':' + str((x+1)*w) + ':' + str((y+1)*h),
		svg]
	jobs.append(subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

for y in range(len(rows)):
	for x in range(len(cols)):
		extract(x, y+4, rows[y] + '_' + cols[x])

extract(13, 0, 'draw4')
extract(13, 4, 'choose')

print('Creating ', len(jobs), 'files ...')

for name, job in zip(names, jobs):
	job.wait()
	print(name + '.png created')
		
importcode = open('importcode.py', 'w')
mlen = max([ len(name) for name in names ])
importcode.write('fileDict = {\n')
for name in names:
	importcode.write("    '" + name + "'" + ' ' * (mlen-len(name)) + " : 'unoCards/" + name + ".png',\n")
importcode.write('}\n')	

sys.exit(0)
