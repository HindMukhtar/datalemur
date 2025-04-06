import re 

# %% 
# Faster method if we can use imported library 
def isPalindromeFast(phrase):
  phrase = re.sub('[^A-Za-z0-9]+', '', phrase)
  if phrase.replace(' ', '').lower() == phrase[::-1].replace(' ', '').lower() : 
    return True 
  else:
    return False

# More memory efficient method that doesn't create a copy   
# %% 
def isPalindrome(phrase):
    left = 0 
    right = len(phrase) - 1
    while left < right: 
        if not phrase[left].isalnum(): 
            left += 1 
            continue
        if not phrase[right].isalnum(): 
            right -= 1 
            continue
        if phrase[right].lower() != phrase[left].lower(): 
            return False 
        right -=1
        left +=1 
    return True
