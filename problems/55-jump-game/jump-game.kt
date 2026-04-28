class Solution {
    fun canJump(nums: IntArray): Boolean {
        var curJump = nums[0] - 1

        if (nums.size > 1 && curJump < 0) return false

        for(i in 1..nums.size - 2){
            curJump = maxOf(curJump, nums[i])
            curJump--
            if(curJump < 0) return false
        }
        return true
    }
}
