/**
 * Definition for a binary tree node.
 * class TreeNode(var `val`: Int = 0) {
 *     var left: TreeNode? = null
 *     var right: TreeNode? = null
 * }
 */

class Solution {
    fun lowestCommonAncestor(root: TreeNode?, p: TreeNode?, q: TreeNode?): TreeNode? {
        if(root == null) return null

        val mini = minOf(p!!.`val`, q!!.`val`)
        val maxi = maxOf(p!!.`val`, q!!.`val`)

        if(root!!.`val` >= mini && root!!.`val` <= maxi) return root
        if(root!!.`val` < mini) return lowestCommonAncestor(root!!.right, p, q)
        return lowestCommonAncestor(root!!.left, p, q)
    }
}
