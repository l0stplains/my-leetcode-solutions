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
    fun kthSmallest(root: TreeNode?, k: Int): Int {
        var ans = -1
        var curPos = 0
        fun find(root: TreeNode?)  {
            if(ans != -1) return
            if(root == null) return
            find(root!!.left)
            curPos++
            if(curPos == k) {
                ans = root!!.`val`
                return
            }
            find(root!!.right)
        }

        find(root)
        return ans
    }
}
