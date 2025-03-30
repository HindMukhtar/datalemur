import numpy as np

def triangular_sum(nums: list) -> int:
  """
    The triangular sum of nums is the value of the only element present in nums after the following process terminates:

    Let nums comprise of n elements. If n == 1, end the process. Otherwise, create a new integer array newNums of length n - 1.
    For each index i, assign the value of newNums[i] as (nums[i] + nums[i+1]) % 10, where % denotes the modulo operator.
    Replace the array nums with newNums.
    Repeat the entire process starting from step 1.
    Return the triangular sum of nums.
  """
  # if nums is a list with a single number, then return that number 
  if len(nums) == 1 :
    return nums[0]; 
  # otherwise, loop around until you get the last remaining item 
  else: 
    newNums = np.zeros(len(nums) - 1)
    while len(newNums) > 0: 
      for i in range(len(newNums)): 
        newNums[i] = (nums[i] + nums[i+1])%10 
      nums = newNums 
      newNums = np.zeros(len(nums) - 1)
  return nums
