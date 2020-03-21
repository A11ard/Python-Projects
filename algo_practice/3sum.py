
from collections import Counter

def threeSum( nums ) :
    """
    :type nums: List[int]
    :rtype: List[List[int]]
    """
    c = Counter(nums)
    for i in c:
        print(i , c[i])

threeSum([1,2,34,5,1,3,22,22,2,2])
