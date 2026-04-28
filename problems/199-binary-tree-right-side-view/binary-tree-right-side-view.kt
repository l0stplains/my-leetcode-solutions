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
    fun rightSideView(root: TreeNode?): List<Int> {
        val ans = mutableListOf<Int>()
        if (root == null) return ans

        val q = ArrayDeque<TreeNode>()
        q.add(root!!)
        while(q.size != 0){
            for(i in 1..q.size - 1){
                val temp = q.removeFirst()
                if(temp.left != null) q.addLast(temp.left)
                if(temp.right != null) q.addLast(temp.right)
            }
            val temp = q.removeFirst()
            ans.add(temp.`val`)
            if(temp.left != null) q.addLast(temp.left)
            if(temp.right != null) q.addLast(temp.right)
        }

        return ans
    }
}
