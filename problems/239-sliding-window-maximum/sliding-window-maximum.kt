class Solution {
    fun maxSlidingWindow(nums: IntArray, k: Int): IntArray {
        val dq = ArrayDeque<Int>()

        var ans = IntArray(nums.size - k + 1)

        for(i in 0..k-1){
            var cur = nums[i]
            while(!dq.isEmpty() && cur > dq.last()){
                dq.removeLast()
            }
            dq.addLast(cur)
        }

        var l = 0
        var r = k - 1

        while(r < nums.size){
            ans[l] = dq.first()
            var curl = nums[l]
            if(dq.first() == curl){
                dq.removeFirst()
            }
            l++
            r++
            if(r >= nums.size) break
            var curr = nums[r]
            while(!dq.isEmpty() && curr > dq.last()){
                dq.removeLast()
            }
            
            dq.addLast(curr)
            
        }

        return ans
    }
}
