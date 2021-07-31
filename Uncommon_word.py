import collections

def uncommon(str1, str2):
    ds = collections.defaultdict(int)
    str1 = str1.split()
    str2 = str2.split()
    ls = []
    for i in str1:
        if i not in ds.keys():
            ds[i] = 1
        else:
            ds[i] += 1

    for j in str2:
        if j in ds.keys():
            ds[j] -= 1
        else:
            ds[j] = 1

    for k,v in ds.items():
        if v >0:
            ls.append(k)         
    return ls

print(none_replace('ace is boy','ace is not boy'))
