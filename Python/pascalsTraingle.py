def generate(numRows):
  """
  Given an integer numRows, return the first numRows of Pascal's triangle
  In Pascal's triangle, each number is the sum of the two numbers directly above it
  """
  pascal_list = [] 
  for i in range(numRows): 
    # start every row with 1s 
    inner_list = [1]*(i+1)
    for j in range(1, i): 
      # set each number to equal the sum of the two numbers above it, exluding edge cases 
      inner_list[j] = pascal_list[i-1][j-1] + pascal_list[i-1][j]
    pascal_list.append(inner_list)
  return pascal_list