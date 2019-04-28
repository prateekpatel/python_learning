class linkedlist:
    def __init__(self, value, Next=None):
        self.value = value
        self.Next = Next


Node1 = linkedlist("3")
# print(Node1.value)
Node2 = linkedlist("4")
Node3 = linkedlist("5")

Node1.Next = Node2
# print(Node1.value)

Node2.Next = Node3

currentNode = Node1
while True:
    print(currentNode.value, end=",")
    if currentNode.Next is None:
        print("None---  On the lst Node")
        break

    currentNode = currentNode.Next


