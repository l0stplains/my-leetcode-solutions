class Solution {
    fun lastStoneWeight(stones: IntArray): Int {
        val maxHeap = PriorityQueue<Int>(compareByDescending {it})

        for(w in stones){
            maxHeap.add(w)
        }

        while(maxHeap.size > 1){
            val a = maxHeap.poll()
            val b = maxHeap.poll()

            if(a != b){
                val c = maxOf(a, b) - minOf(a, b)
                maxHeap.add(c)
            }
        }
        return maxHeap.poll() ?: 0


    }
}
