# Write a function that takes an ordered list of numbers (a list where the elements are in order from smallest to largest) 
# and another number. The function decides whether or not the given number is inside the list and returns (then prints) 
# an appropriate boolean.

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
