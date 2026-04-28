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


    fun isTarget(node: TreeNode?, target: Int): Boolean {
        if(node == null) return false

        return node.left == null && node.right == null && node.`val` == target
    }

    fun removeLeafNodes(root: TreeNode?, target: Int): TreeNode? {
        if(root == null) return root

        root.left = removeLeafNodes(root.left, target)
        root.right = removeLeafNodes(root.right, target)

        if(isTarget(root, target)) return null

        return root
    }
}
