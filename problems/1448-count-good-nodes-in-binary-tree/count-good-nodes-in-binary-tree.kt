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
    fun goodNodes(root: TreeNode?): Int {
        return count(root, Int.MIN_VALUE)
    }

    private fun count(root:TreeNode?, maks: Int): Int {
        if(root == null) return 0
        var res = 0
        var curMaks = maks
        if(root!!.`val` >= maks) {
            res++
            curMaks = root!!.`val`
        }

        return res + count(root!!.left, curMaks) + count(root!!.right, curMaks)
    }
}
