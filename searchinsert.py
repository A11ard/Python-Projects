def searchInsert( nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: int
    """
    s = 0
    e = len(nums)-1
    while s + 1 < e:
        #print(s,e)
        if nums[(s+e)//2] > target:
            e = (s+e)//2
        elif nums[(s+e)//2] < target:
            s = (s+e)//2
        else:
            return (s+e)//2
    #print(s,e)
    if nums[s] >= target:
        return s
    elif nums[e] < target:
        return e+1
    else:
        return s+1


print(searchInsert([1,3,5,6],0))
print(searchInsert([1,3,5,6],2))
print(searchInsert([1,3,5,6],3))
print(searchInsert([1,3,5,6],5))
print(searchInsert([1,3,5,6],6))
print(searchInsert([1,3,5,6],7))
