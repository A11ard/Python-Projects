# some a x b matrix populated by 1 or 0
# find the largest square of 1 inside the matrix
import random

def make_matrix(r,c): #make r x c matrix
    ret = []
    for row in range(r):
        temp = []
        for col in range(c):
            temp.append(random.randint(0,1))
        ret.append(temp)
    return ret
def print_matrix(matrix):
    for row in matrix:
        print(row)
def blank_matrix(r,c,value):
    ret = []
    for row in range(r):
        temp = []
        for col in range(c):
            temp.append(value)
        ret.append(temp)
    return ret

def solve(im):
#ultimately this is O(r*c) , memory (r * c)
#uses a 2D memoize matrix
    dp = blank_matrix(len(im)+1,len(im[0])+1,0) #this is is r+1 x c+1 so there is a "cushion" of zeros in the top and left border
    maxlength = 0
    rc = (0,0)
    for r in range(1,len(im)+1):
        for c in range(1,len(im[0])+1):
            if im[r-1][c-1] == 1:
                dp[r][c] = min(dp[r-1][c-1] , min(dp[r-1][c], dp[r][c-1])) + 1
                if dp[r][c] > maxlength:
                    maxlength = dp[r][c]
                    rc = (r,c) #rc will be the tuple with the coordinate of the bottom right corner of squar
    return [maxlength, rc]

def solve_better(im):
    #same big O, memory is just (c)
    dp = [0 for i in range(len(im[0])+1)] #dp is 1D array of length equal to number of columns
    maxlength = 0
    prev = 0
    rc = (0,0)
    for r in range(1,len(im)+1):
        for c in range(1,len(im[0])+1):
            temp = dp[c]
            if im[r-1][c-1] == 1: #have to do an evaluation to see if this a bottom right corner
                dp[c] = min(dp[c-1] , min(dp[c], prev)) + 1
                if dp[c] > maxlength:
                    maxlength = dp[c]
                    rc = (r,c) #rc will be the tuple with the coordinate of the bottom right corner of squar
            else:
                dp[c] = 0
            prev = temp
    return [maxlength, rc]

def solve_better1(im):
    #same big O, memory is just (c)
    dp = [0 for i in range(len(im[0])+1)] #dp is 1D array of length equal to number of columns
    maxlength = 0
    prev = 0
    rc = (0,0)
    for r in range(1,len(im)+1):
        for c in range(1,len(im[0])+1):
            if im[r-1][c-1] == 1: #have to do an evaluation to see if this a bottom right corner
                temp = prev
                prev = min(dp[c-1] , min(dp[c], prev)) + 1
                if dp[c] > maxlength:
                    maxlength = dp[c]
                    rc = (r,c) #rc will be the tuple with the coordinate of the bottom right corner of squar
                dp[c-1] = temp
                if c == len(im[0]):
                    dp[c] = prev
                    prev = 0
            else:
                prev = 0
    return [maxlength, rc]


for i in range(1000):
    x = make_matrix(10,16)
    if solve(x)[0] == solve_better(x)[0] and solve_better(x)[0] >= 3:
        print_matrix(x)
        print(solve(x))
        print(solve_better1(x), "                               ", solve(x)[1] == solve_better(x)[1])
