/**
 * Example:
 * var ti = TreeNode(5)
 * var v = ti.`val`
 * Definition for a binary tree node.
 * class TreeNode(var `val`: Int) {
 *     var left: TreeNode? = null
 *     var right: TreeNode? = null
 * }
 */
class Solution {
    fun invertTree(root: TreeNode?): TreeNode? {
        val dq = ArrayDeque<TreeNode>()
        if(root != null) dq.addLast(root!!)

        while(!dq.isEmpty()){
            val cur = dq.removeFirst()
            var temp = TreeNode()
            temp = cur.left
            cur.left = cur.right
            cur.right = temp

            if(cur.left != null) dq.addLast(cur.left!!)
            if(cur.right != null) dq.addLast(cur.right!!)
        }

        return root
    }
}
