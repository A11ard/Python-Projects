def generateParenthesis(n):
    if n == 0:
        return [""]
    else:
        ret = []
        def help(x,current,stack_ct): #n is the number of pairs left and stack_ct tracks how much parenthesis i still need
            if x == 0 and stack_ct == 0:
                ret.append( current )
            else:
                if x != 0:
                    if stack_ct > 0:
                        help(x, current+")" , stack_ct-1)
                        help(x-1, current+"(", stack_ct+1)
                    else:
                        help(x-1, current+"(", stack_ct+1)
                else: #this means stack_ct != 0 AND x == 0
                    for i in range(stack_ct):
                        current += ")"
                    ret.append(current)
        help(n-1,"(",1)
        return ret

generateParenthesis(1)

# help(x, current+")" , stack_ct-1)
# help(x-1, current+"(", stack_ct+1)
