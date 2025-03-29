def another_one(digits):
  """
  Return an array of digits of the number after adding another one to the input
  """
  # convert list of integers to list of strings then concatenate them to a single string 
  # convert string back to int value and add 1 
  num = int("".join(map(str,digits))) + 1
  # convert integer back to list of integers 
  num_str = list(str(num))
  return list(map(int, num_str))