def simplesearch(alist,anum):
    for i in alist:
        if i == anum:
            return True
        
    return False

if __name__ == "__main__":
    
    alist = input('Enter list ')
    anum = input('Enter number ')
    searchresult = simplesearch(alist,anum)
    print(searchresult)
