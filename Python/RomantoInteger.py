def romanToInt(s):
  """
  Given a valid Roman numeral, convert it to an integer
  """
  # Create dictionary to map roman numerals to integer value 
  roman_dict = {"I": 1,"V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
  num = []
  first_num = 0 
  total = first_num
  subtract = 0 
  for i in range(len(s)-1): 
    # Check if next value is greater than current value 
    try: 
        if roman_dict[s[i]] >= roman_dict[s[i+1]]: 
            total +=  roman_dict[s[i]] - subtract
            subtract = 0 
        # If it is then subtract 
        else: 
            subtract = roman_dict[s[i]]
    except Exception as e: 
       print(f"Roman numeral {s[i]} is not valid")
  total += roman_dict[s[len(s)-1]] - subtract

  return total