class Solution {
    fun search(nums: IntArray, target: Int): Int {
        var l = 0
        var r = nums.size - 1

        var i = 0
        while (l <= r){
            i = (r + l) / 2
            var cur = nums[i]
            when {
                cur > target -> { r = i - 1 }
                cur < target -> { l = i + 1 }
                cur == target -> { return i }
            }
        }

        return  -1
    }
}
