def permute(nums):
    """
    :type nums: List[int]
    :rtype: List[List[int]]
    """
    ret = []
    def helper(saved, remain ):
        #add the finished to ret
        if len(remain) == 0:
            ret.append(saved)
        else:
            for i in range(len(remain)):
                rtemp = remain.copy()
                stemp = saved.copy()
                stemp.append(rtemp.pop(i))
                helper(stemp, rtemp)
    helper([],nums)
    return ret

print(len(permute([1,2,3,4])))
