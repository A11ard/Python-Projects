def lengthOfLastWord( s):
    if len(s) == 0:
        return 0
    count = 0
    last = len(s)-1
    while s[last] == " ":
        last -= 1
        if last < 0:
            return 0
    for i in range(last, -1, -1):
        if s[i] == " ":
            return count
        count += 1
    return count

print(lengthOfLastWord("Hello world"))
print(lengthOfLastWord("Hello world     "))
print(lengthOfLastWord("  world  "))
print(lengthOfLastWord("   a  "))
print(lengthOfLastWord(""))
