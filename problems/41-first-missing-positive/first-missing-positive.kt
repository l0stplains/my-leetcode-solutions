class Solution {
    fun firstMissingPositive(nums: IntArray): Int {
        var find = false
        for(i in 0..nums.size-1){
            if(!find && nums[i] == 1){
                find = true
            }
            if(nums[i] <= 0){
                nums[i] = 1
            } 
        }
        if(!find) return 1

        for(i in 0..nums.size-1){
            val cur = abs(nums[i])
            if(cur > nums.size) continue
            if(nums[cur - 1] > 0) nums[cur - 1] = -1 * nums[cur - 1]
        }

        for(i in 0..nums.size-1){
            if(nums[i] > 0){
                return i + 1
            }
        }
        return nums.size + 1
    }
}
