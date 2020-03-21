from math import gcd
def nthMagicalNumber( N, A, B):
    """
    :type N: int
    :type A: int
    :type B: int
    :rtype: int
    """
    def helper(num):
        return (num // A) + (num // B) - (num // (A*B / gcd(A,B)))
    lo = 0
    hi = max(A*N , B*N)
    while lo < hi:
        mid = (lo + hi) // 2
        print(mid, helper(mid) )
        if helper(mid) < N:
            lo = mid+1
        else:
            hi = mid
    return lo

print(nthMagicalNumber(8,10,5)) # 2 4 6 8 10
