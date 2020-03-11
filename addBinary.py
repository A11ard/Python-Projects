def addBinary(a, b):
    """
    :type a: str
    :type b: str
    :rtype: str
    """
    return str(bin(int("0b"+a , 2) + int("0b"+b,2)))[2:]


print(addBinary("11","1"))
