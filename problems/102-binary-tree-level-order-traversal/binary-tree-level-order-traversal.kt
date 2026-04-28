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
    fun levelOrder(root: TreeNode?): List<List<Int>> {
        val res = mutableListOf<MutableList<Int>> ()

        if(root == null) return res
        var q = mutableListOf<TreeNode>()
        q.add(root!!)
        while(q.size != 0){
            val temp = mutableListOf<TreeNode>()
            val ans = mutableListOf<Int>()
            for(i in 0..q.size - 1){
                ans.add(q[i].`val`)
                if(q[i].left != null) temp.add(q[i].left!!)
                if(q[i].right != null) temp.add(q[i].right!!)
            }

            res.add(ans)
            q = temp
        }
        return res
    }
}
