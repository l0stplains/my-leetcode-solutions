

class KthLargest(k: Int, nums: IntArray) {

    val maxHeap = PriorityQueue<Int>(compareByDescending{ it })
    val minHeap = PriorityQueue<Int>() 
    var selfK = 0

    init {
        selfK = k
        for(x in nums){
            if(minHeap.size < k) minHeap.add(x)
            else {
                val top = minHeap.peek()!!

                if (top < x) {
                    minHeap.poll()
                    minHeap.add(x)
                    maxHeap.add(top)
                } else {
                    maxHeap.add(x)
                }
            }
        }
    }

    fun add(`val`: Int): Int {

        if(minHeap.size < selfK) {
            minHeap.add(`val`)
            return minHeap.peek()
        }
        val top = minHeap.peek()
        
        if (top < `val`) {
            minHeap.poll()
            minHeap.add(`val`)
            maxHeap.add(top)
        } else {
            maxHeap.add(`val`)
        }

        return minHeap.peek()!!
    }

}

/**
 * Your KthLargest object will be instantiated and called as such:
 * var obj = KthLargest(k, nums)
 * var param_1 = obj.add(`val`)
 */
