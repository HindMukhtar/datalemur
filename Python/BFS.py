from collections import dequeue
def bfs(root): 
    # use queue 
    q = dequeue[root]
    while q: 
        node = q.popleft() 
        if node.left: 
            q.append(node.left)
        if node.right: 
            q.append(node.right)