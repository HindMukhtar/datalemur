def is_same_stripes(matrix: list) -> bool:
  """
  Function to determine if the matrix has diagonal stripes 
  where all elements in each diagonal from top-left to bottom-right are of the same stripe—that is, 
  they are identical
  """
  # dictionary to store diagonal values
  # i-j is the same value for every item in the diagonal
  diagonals = {} 
  for i in range(len(matrix)): 
    for j in range(len(matrix[i])):
      # If values are diagonal but values are not the same then return false 
      if i-j in diagonals and diagonals[i-j] != matrix[i][j]: 
        return False 
      # Otherwise assign to daigonal dictionary to keep track 
      else: 
        diagonals[i-j] = matrix[i][j]
  return True 
