#!/usr/bin/python3
import sys, subprocess

svg = 'cards.svg'

pw = subprocess.Popen(['inkscape', '-W', svg], stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
ph = subprocess.Popen(['inkscape', '-H', svg], stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)

pw.wait()
ph.wait()

w = float(pw.stdout.read()) / 13
h = float(ph.stdout.read()) / 5

rows = [ 'spade', 'heart', 'diamond', 'club' ]
cols = [ 'ace' ] + [ str(x) for x in range(2,11) ] + [ 'jack', 'queen', 'king' ]

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
		extract(x, y+1, rows[y] + '_' + cols[x])

extract(0, 0, 'black_joker')
extract(1, 0, 'red_joker')
extract(2, 0, 'back')

print('Creating ', len(jobs), 'files ...')

for name, job in zip(names, jobs):
	job.wait()
	print('created ' + name + '.png created')
		
importcode = open('importcode.py', 'w')
mlen = max([ len(name) for name in names ])
importcode.write('fileDict = {\n')
for name in names:
	importcode.write("    '" + name + "'" + ' ' * (mlen-len(name)) + " : 'frenchCards/" + name + ".png',\n")
importcode.write('}\n')	

sys.exit(0)
