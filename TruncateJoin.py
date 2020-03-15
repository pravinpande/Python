#Given a string of even length, return the first half. So the string "WooHoo" yields "Woo".
#first_half('WooHoo') → 'Woo'
#first_half('HelloThere') → 'Hello'
#first_half('abcdef') → 'abc'
def first_half(str):
  p = []
  for i in range(int(len(str)/2)):
  	p.append(str[i])
  b = ''.join(p)
  return b

print(first_half('woohoo'))
