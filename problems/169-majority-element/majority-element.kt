class Solution {
    fun majorityElement(nums: IntArray): Int {
        var cur: Int? = null
        var cnt = 0

        for(i in 0..nums.size-1){
            if(cur == null){
                cur = nums[i]
                cnt = 1
                continue
            }
            if(cur!! == nums[i]) cnt++
            else {
                cnt--
                if(cnt == 0) cur = null
            }
        }

        return cur!!
    }
}
