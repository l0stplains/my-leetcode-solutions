class Solution {
    fun maxSubArray(nums: IntArray): Int {
        var cur = 0
        var ans = nums[0]

        for(num in nums){
            cur += num
            ans = maxOf(ans, cur)
            if(cur < 0) cur = 0
        }

        return ans
    }
}
