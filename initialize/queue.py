class Node:
  def __init__(self, content=None, path=None, id=None):
    self.next = None
    self.content = content
    self.path = path
    self.id = id

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, element):
        self.queue.append(element)

    def dequeue(self):
        if self.isEmpty():
            return "Queue vacía."
        return self.queue[0]
    
    def size(self):
        return len(self.queue)
    
    def peek(self):
        if self.isEmpty():
            return "Queue vacía"
        return self.queue[0]
    
    def isEmpty(self):
        return len(self.queue) == 0