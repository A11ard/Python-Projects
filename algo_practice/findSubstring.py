from collections import Counter

def findSubstring( s, words):
    """
    :type s: str
    :type words: List[str]
    :rtype: List[int]
    """
    length = sum(len(i) for i in words)
    ret = []
    r = 0
    c = Counter(words)
    while r + length < len(s)+1:
        c1 = Counter( s[r + i*len(words[0]) : r + (i+1)*len(words[0]) ]  for i in range(len(words)) )
        if c == c1:
            ret.append(r)
        r += 1
    return ret

print(findSubstring("wordgoodgoodgoodbestword" , ["word","good","best","good"]))
