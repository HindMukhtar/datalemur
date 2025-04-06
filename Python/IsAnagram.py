def is_anagram(s, t):
    """
    Given two strings s and t
    return True if the two strings are anagrams of each other
    otherwise return False

    An anagram is a word or phrase formed by rearranging the letters of 
    a different word or phrase, using all the original letters exactly once
    """
    s_dict = {char: idx+1 for idx, char in enumerate(s)}
    t_dict = {char: idx+1 for idx, char in enumerate(t)}
    if (s_dict.keys() == t_dict.keys()): 
        return True
    else: 
        return False