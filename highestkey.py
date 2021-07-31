import collections

def none_replace(dict1):
    ds = collections.defaultdict(list)
    for i,j in dict1.items():
    	ds[j].append(i)
  	x = sorted(ds.items())
  	return x

print(none_replace({'a':5 , 'b':4, 'c':3, 'd':3, 'e':1, 'a':6}))
