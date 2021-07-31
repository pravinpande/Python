def replace1(ls):
    ls1 = []
    for i in range(len(ls)):
        if ls[i] == None:
            ls1.append(ls[i-1])
        else:
            ls1.append(ls[i])
    return ls1

print(replace1([1,2,3,None]))
