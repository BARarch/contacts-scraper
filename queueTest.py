import queue

q = queue.LifoQueue()
for i in range(5):
    q.put(i)
    
for i in range(5):
    print(q.get(0))
    