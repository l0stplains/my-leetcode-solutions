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
    var ans = 0
    
    fun diameterOfBinaryTree(root: TreeNode?): Int {
        maxHeight(root)
        return ans
    }
    fun maxHeight(root: TreeNode?): Int {
        if(root == null) return 0

        var res = 0
        val l = maxHeight(root!!.left)
        var r = maxHeight(root!!.right)

        ans = maxOf(ans, l + r)
        res = maxOf(l, r)

        return 1 + res
    }
}
