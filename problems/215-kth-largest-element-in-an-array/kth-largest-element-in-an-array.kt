class Solution {
    fun findKthLargest(nums: IntArray, k: Int): Int {
        val minHeap = PriorityQueue<Int>()

        for(n in nums){
            if(minHeap.size < k) minHeap.add(n)
            else {
                val top = minHeap.peek()
                if(top < n){
                    minHeap.poll()
                    minHeap.add(n)
                }
            }
        }

        return minHeap.peek() ?: 0
    }
}
