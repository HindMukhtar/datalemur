def fizz_buzz_sum(target: int) -> int:
  """
  Function that finds all multiples of 3 and 5 below a target value
  """
  # Create a list of numbers from 0 to target 
  num_list = list(range(target))
  # Find modulu 3 for every item in the list 
  mod3 = [i%3 for i in num_list]
  # If i%3 is 0, then its a multiple
  three = [index for index, element in enumerate(mod3) if element == 0]
  # Repeat for 5 
  mod5 = [i%5 for i in num_list]
  five = [index for index, element in enumerate(mod5) if element == 0]
  # Convert to set to remove duplicates, union both and return sum 
  union = list(set(three).union(five))
  return sum(union)
