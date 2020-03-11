

# You will be given, for each letter of the alphabet, the
# number of campers whose last names start with that letter.
# You will also be given the number of registration tables.
# minimize campers assigned to busiest table

roster1 = [32,21,18,25,38,50,14,18,25]

def helper(roster, num_tables, lim): #given the roster, can you divide it into the number of tables and have each table have less than the limit?
    index = [0]
    #roster.append(lim+1)
    for i in range(num_tables): # for this next table
        temp = 0
        for x in range(index[-1], len(roster)): # try to fill the table below the limit
            if temp + roster[x] <= lim:
                temp += roster[x]
                if x == len(roster) - 1:
                    print(index)
                    return True
            else:
                index.append(x)
                temp = 0
                break
    print(index)
    return False

def solve(roster, num_tables):
    end = sum(roster)
    start = 0
    mid = int((end + start)/2.0)
    prev = []
    mids = []
    while True: #this is the bin search
        val = helper(roster, num_tables, mid)
        if val: #got true, go down
            temp = end # save end
            end = mid
        else: # got false, go up
            temp = start #save start
            start = mid
        mid = (end+start)//2
        prev.append(val)
        mids.append(mid)
        try:
            #if (prev[-1] ^ prev[-2]) and (prev[-3] ^ prev[-4]):
            if mids[-1] == mids[-2] and mids[-2] == mids[-3]:
                print("mids ",mids, "end:", end , ";  start:",start)
                return mid
        except:
            pass


print(helper(roster1, 5, 50))

print(solve(roster1, 5))
