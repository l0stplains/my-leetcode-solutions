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
    fun maxDepth(root: TreeNode?): Int {
        var ans = 0
        if(root == null) return 0
        var dq = ArrayDeque<TreeNode>()
        dq.addLast(root!!)
        while(!dq.isEmpty()){
            for(i in 1..dq.size){
                val cur = dq.removeFirst()
                if(cur.left != null) dq.addLast(cur.left!!)
                if(cur.right != null) dq.addLast(cur.right!!)
            }
            ans++
        }

        return ans
    }
}
