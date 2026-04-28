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
    fun insertLeft(root: TreeNode?, node: TreeNode): TreeNode {
        if(root == null) return node

        root!!.left = insertLeft(root!!.left, node)
        return root!!
    }

    fun deleteNode(root: TreeNode?, key: Int): TreeNode? {
        var temp = root
        if (root == null) return null
        if(key > root!!.`val`) root!!.right = deleteNode(root!!.right, key)
        else if (key < root!!.`val`) root!!.left = deleteNode(root!!.left, key)
        else  {
            if(root!!.right != null){
                temp = root!!.right
                if(root!!.left != null) insertLeft(temp, root!!.left!!)
            } else temp = root!!.left
        }

        return temp
    }
}
