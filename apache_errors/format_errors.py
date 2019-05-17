with open('errors.txt') as f:
	s = f.read()
with open('errors.txt', 'w') as f:
	f.write('\n'.join(([i.split(']')[-1] for i in s.split('\n')])))
