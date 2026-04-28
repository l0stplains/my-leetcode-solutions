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
    fun isSubtree(root: TreeNode?, subRoot: TreeNode?): Boolean {
        if(isTreeSame(root, subRoot)) return true
        if(root == null) return false
        return isSubtree(root!!.left, subRoot) || isSubtree(root!!.right, subRoot)
        
    }

    fun isTreeSame(a: TreeNode?, b: TreeNode?): Boolean {
        if(a == null && b == null) return true
        if(a == null) return false
        if(b == null) return false

        return a!!.`val` == b!!.`val` && isTreeSame(a!!.left, b!!.left) && isTreeSame(a!!.right, b!!.right)
    }
}
