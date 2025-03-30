from collections import Counter

def contains_duplicate(input)-> bool:
  """
  Given an list of integers called input: 
  Return True if any value appears at least twice in the array
  Return False if every element in the input list is distinct
  """
  # Create counter, convert to dict to exract counter values, then insert counts into a list 
  input_dict = list(dict(Counter(input)).values())
  if sum(input_dict) > len(input_dict): 
    return True 
  else: 
    return False
