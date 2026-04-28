class Solution {
    private fun euclidDistance(x: Double, y: Double): Double{
        return sqrt(x * x + y * y)
    }
    fun kClosest(points: Array<IntArray>, k: Int): Array<IntArray> {
        val maxHeap = PriorityQueue<Pair<Double, IntArray>>(compareByDescending {it.first} )

        for(p in points){
            val cur = (euclidDistance(p[0].toDouble(), p[1].toDouble()) to p)
            if(maxHeap.size < k) maxHeap.add(cur)
            else {
                val top = maxHeap.peek()
                if (top.first > cur.first){
                    maxHeap.poll()
                    maxHeap.add(cur)
                }
            }
        }
        val ans = mutableListOf<IntArray>()
        while(maxHeap.size != 0){
            val cur = maxHeap.poll()
            ans.add(cur.second)
        }

        return ans.toTypedArray()
    }
}
