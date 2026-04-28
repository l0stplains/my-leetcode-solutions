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
    var ans = true
    fun isBalanced(root: TreeNode?): Boolean {
        sol(root)
        return ans
    }

    fun sol(root: TreeNode?): Int {
        if(root == null) return 0

        val l = sol(root.left)
        val r = sol(root.right)

        if(abs(l - r) > 1) ans = false

        return 1 + maxOf(l, r)


    }
}
