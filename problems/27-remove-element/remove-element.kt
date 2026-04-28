class Solution {
    fun removeElement(nums: IntArray, `val`: Int): Int {
        var k = 0
        for(i in nums.size-1 downTo 0){
            if(nums[i] == `val`){
                k++
                val temp = nums[nums.size - k]
                nums[nums.size - k] = nums[i]
                nums[i] = temp
            }
        }

        return nums.size - k
    }
}
