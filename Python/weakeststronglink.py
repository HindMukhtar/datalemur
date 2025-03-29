def weakest_strong_link(strength: list) -> int:
  """
  Given a matrix strength, 
  return the weakest strong link if it exists; 
  otherwise, return -1. 
  If a weakest strong link exists, 
  it is always exactly one, 
  and it can be proven that no other link will satisfy both conditions simultaneously.
  """
  for i in range(len(strength)):  # Iterate over rows
      row = strength[i]  # Get the i-th row
      # get weakest value in the row 
      weak = min(row)
      for j in range(len(row)):  # Iterate over columns in the current row
          col = [strength[k][j] for k in range(len(strength))]  # Get the entire j-th column
          # get strongest value in the column 
          strong = max(col)
          if strength[i][j] == weak and strength[i][j] == strong: 
            return strength[i][j]
  return -1