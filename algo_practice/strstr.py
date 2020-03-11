
def strStr( haystack, needle):
    if len(needle) == 0:
        return 0
    try:
        return haystack.index(needle)
    except:
        return -1


print(strStr("asdfasdf", "fta"))
