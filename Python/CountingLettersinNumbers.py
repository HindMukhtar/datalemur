def mapnum(n):
  """
  Helper function for total_letters 
  """  

  # dictionary containing the spelling of each number 
  word_dict = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 
    7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven",12: "twelve", 13: "thirteen", 
    14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 
    19: "nineteen", 20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 
    60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety", 100: "hundred"
  } 

  # convert number to written words   
  if (n <= 20):
    return word_dict[n]
  elif (n < 100) and (n%10 == 0): 
    return word_dict[n]
  elif (n == 100): 
    n1 = n//100
    n2 = n%100
    return word_dict[n1] + word_dict[n1*100]
  elif n > 20 and n <100:  
    n1 = n//10
    n2 = n%10
    return word_dict[n1*10] + word_dict[n2]
  elif (n > 100): 
    n1 = n//100
    n2 = n%100
    return word_dict[n1] + word_dict[n1*100] + "and" + word_dict[n2]
    
    
def total_letters(N):
  """
  Function that takes list of number, converts it to written words then counts the number of letters for all of them 
  """
  num_list = [i+1 for i in range(N)]
  numword = [mapnum(num) for num in num_list]
  numword = "".join(numword)

  return len(numword)