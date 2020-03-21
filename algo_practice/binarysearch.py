from random import randint, choice

def make_testcase():
    size = randint(0, 10000)
    return sorted([randint(0, 10000) for _ in range(size)])

def test(fxn):
    for _ in range(15):
        inp = make_testcase()
        query = choice(inp)

        correct = inp.index(query)

        assert fxn(inp, query) == correct


def solve(arr, element):
    lo = 0
    hi = len(arr)-1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < element:
            lo = mid + 1
        else:
            hi = mid
    return lo

test(solve)

print(solve([0,1,2,3,4,5,6,7,8,9,9,9,9,10,13,14],9))
