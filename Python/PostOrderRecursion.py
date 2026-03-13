# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def PreOrder(self, root): 
        stack = [root] 

        while stack: 
            node = stack.pop() 
            # viist(node)
            if node.right: 
                stack.append(node.right)
            if node.left: 
                stack.append(node.left)

    def dfs_preorder(self, root):
        node = root  
        if not node: 
            return 
        # visit node 
        if node.left: self.dfs_preorder(node.left)
        if node.right: self.dfs_preorder(node.right)

    def dfs_postorder(self, root): 
        node = root
        if not node: 
            return 
        if node.left: self.dfs_postorder(node.left)
        if node.right: self.dfs_postorder(node.right)
        # visit(node)

    def TwoStackPostOrder(self, root):
        # Post order traversal 
        stack1 = [root]
        stack2 = [] 

        # Get the nodes in the correct order 
        # root -> right -> left 
        while stack1: 
            node = stack1.pop()
            stack2.append(node)
            if node.right: 
                stack1.append(node.right)
            if node.left: 
                stack1.append(node.left)
                
        # Now post order traverse 
        while stack2: 
            # Now it's in order 
            node = stack2.pop() 
            # visit(node)

    def OneStackPostOrder(self, root): 
        node = root 
        stack = [] 
        last = None 
        while stack or node: 
            if node: 
                stack.append(node)
                node = node.left 

            else:
                peek = stack[-1] #check the last element 
                # if the last element has a right child then visit it 
                if peek.right and peek.right != last: 
                    node = peek.right 
                else: 
                    #visit(peek) # This is the next node in our order 
                    last = stack.pop() 

