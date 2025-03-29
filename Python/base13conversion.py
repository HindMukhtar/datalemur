def convertToBase13(num):
    """
    Given an integer num, return its string representation in base 13
    For 10, 11, 12 use the values A, B and C 
    """
    if num == 0:
        return "0"

    # Digits for base 13
    base13_digits = "0123456789ABC"  
    digits = ""
    positive = abs(num)
    
    while positive > 0:
        # Append digits/letters
        digits += base13_digits[positive % 13]  
        positive = positive // 13

    # Reverse the string at the end
    reversed_digits = digits[::-1]  
    if num < 0:
        return "-" + reversed_digits
    else:
        return reversed_digits