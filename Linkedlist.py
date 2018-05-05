#!/usr/bin/python

class Node(object):
    def __init__(self,elem):
        self.elem=elem
        self.next=None

class LinkedList(object):
    def __init__(self,node=None):
        self.__head=node

    def is_empty(self):
        return self.__head == None

    def length(self):
        count = 0
        cur = self.__head
        while cur != None:
            count = count + 1
            cur = cur.next
        return count

    def travel(self):
        cur = self.__head
        while cur != None:
            print(cur.elem)
            cur = cur.next
        return 1

    def append(self,item):
        node = Node(item)
        cur = self.__head
        if self.__head == None:
            self.__head = node
        else:
            while cur.next !=  None:
                cur=cur.next
            cur.next=node

    def add(self,item):
        node=Node(item)
        node.next=self.__head
        self.__head=node

    def insert(self,pos,item):
        new_node=Node(item)
        cur=self.__head
        current_seq=0
        if pos < self.length():
            while current_seq < pos:
                cur=cur.next
                current_seq += 1
            cur_pri_next=cur.next
            new_node.next=cur_pri_next
            cur.next=new_node
        else:
            print("Pos is wrong")


if __name__ == "__main__":
    ll = LinkedList()
    print(ll.is_empty())
    print(ll.length())
    ll.travel()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.append(4)
    ll.append(5)
    ll.append(6)
    print("Append has finished")
    ll.travel()
    print("add function is as below:")
    ll.add(8)
    ll.travel()
    ll.insert(2,8888)
    print ("After the insert")
    ll.travel()
    ll.insert(22000,88)

