class linkedListNode:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class linkedList:
    def __init__(self, head=None):
        self.head = head

    def insert (self, value):
        node = linkedListNode(value)
        if self.head is None:
            self.head = node
            return

        currentNode = self.head
        while True:
            if currentNode.next is None:
                currentNode.next = node
                break
            currentNode = currentNode.next


    def printLinkedList(self):
        currentNode = self.head
        while currentNode is not None:
            print(currentNode.value,"---", end=",")
            currentNode = currentNode.next
        print("None")


ll = linkedList()
ll.printLinkedList()
ll.insert("3")
ll.printLinkedList()
ll.insert("5")
ll.printLinkedList()
ll.insert("6")
ll.printLinkedList()

