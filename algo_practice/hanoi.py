A = [1,2,3,4,5,6,7]
B = []
C = []

def hanoi(disks, start, end, aux):
    if disks > 0:
        hanoi(disks-1, start, aux, end)
        end.append(start.pop())
        print(A, B, C)
        hanoi(disks-1, aux, end, start)

def test_hanoi(start, end, aux):
    disks = len(start)
    moves = []
    def h(d, start, end, aux):
        if d > 0:
            h(d-1, start, aux, end)
            end.append(start.pop())
            moves.append(0)
            h(d-1, aux, end, start)
    h(disks,start,end,aux)
    return len(moves)


#hanoi(7,A,B,C)
#print(test_hanoi(A,B,C))
for i in range(22):
    A = [y for y in range(i+1)]
    B = []
    C = []
    print("number of moves for", i+1, "disks:",test_hanoi(A,B,C))
