#Given a string, return a version without the first and last char, so "Hello" yields "ell". The string length will be at least 2.
#without_end('Hello') → 'ell'
#without_end('java') → 'av'
#without_end('coding') → 'odin'

def without_end(str):
	a = [x for x in str]
	a.remove(a[0])
	a.remove(a[-1])
	b = ''.join(a)
	return b

print(without_end('pravin'))
