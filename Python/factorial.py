def factorial(n):
  """
  Function to get factorial of n 
  """
  fact = 1 
  for i in range(n): 
    fact = fact*(n-i)
  return fact