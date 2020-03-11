#leetcode easy

class ListNode(object):
     def __init__(self, x):
         self.val = x
         self.next = None

class Solution(object):
    def mergeTwoLists(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        if l1 == None:
            return l2
        elif l2 == None:
            return l1
        if l1.val > l2.val:
            ret = l2
            l2 = l2.next
        else:
            ret = l1
            l1 = l1.next
        p = ret
        while True:
            try:
                if l2.val > l1.val: #l1 is smaller, so p goes to l1 next
                    p.next = l1
                    p = l1
                    l1 = l1.next
                else:
                    p.next = l2
                    p = l2
                    l2 = l2.next
            except:
                pass
            if l1 == None:
                p.next = l2
                break
            if l2 == None:
                p.next = l1
                break
        return ret
