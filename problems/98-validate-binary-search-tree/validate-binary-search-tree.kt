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
    fun isValidBST(root: TreeNode?): Boolean {
        fun isValid(root: TreeNode?): Triple<Long, Long, Boolean> { // min, maks, valid
            if(root == null) return Triple(Long.MAX_VALUE, Long.MIN_VALUE, true)

            val (lMin, lMax, lValid) = isValid(root!!.left) 
            val (rMin, rMax, rValid) = isValid(root!!.right)

            val cur = root!!.`val`.toLong()

            val min = minOf(cur, minOf(lMin, rMin))
            val max = maxOf(cur, maxOf(lMax, rMax))
            return Triple(min, max, lValid && rValid && lMax < cur && rMin > cur)
        }
        
        return isValid(root).third
    }
}
