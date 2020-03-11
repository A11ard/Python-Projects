def removeDuplicates(nums):
    if len(nums) <= 1:
        return len(nums)
    toInsert = 0
    for current in range(len(nums)):
        if nums[current] != nums[toInsert]: #move toInsert to next position
            toInsert += 1
            nums[toInsert] = nums[current]
    print(nums)
    return toInsert+1

print(removeDuplicates([0,1,1,1,2]))
print(removeDuplicates([0,1,1,1,2,3,3,3,5]))
print(removeDuplicates([0,1,2,3,3]))
print(removeDuplicates([1,1,1,2]))
print(removeDuplicates([1,1,2]))
