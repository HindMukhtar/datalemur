def intersection(a, b):
  """
  function to get the intersection of two lists
  """
  union = list(set(a) & set(b))
  return union
