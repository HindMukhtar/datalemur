def compound_interest(principal: int, rate: int, contribution: int, years: int) -> float:
  """
  Function to calculate balance given principal, rate, annual contributions and number of year 
  Round balance to the nearest 2 decimals 
  """
  balance = principal
  for i in range(years): 
    balance = balance*(rate/100 + 1)
    balance = balance + contribution
  return round(balance, 2)