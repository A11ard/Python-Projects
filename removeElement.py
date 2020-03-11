def removeElement( nums, val):
    end = len(nums)
    i = 0
    while i < end:
        if nums[i] == val:
            nums[i] = nums[end-1]
            end -= 1
        else:
            i += 1
    return end

def removeElement1(nums, val):
    count = 0
    for i in nums:
        if i != val:
            nums[count] = i
            count += 1
    return count

print(removeElement([2,2,3],2))
print(removeElement([3,3],3))
