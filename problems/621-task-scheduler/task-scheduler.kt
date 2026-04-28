class Solution {
    fun leastInterval(tasks: CharArray, n: Int): Int {
        val dict = mutableMapOf<Char, Int>()

        for(t in tasks){
            dict[t] = (dict[t] ?: 0) + 1
        }

        val pq = PriorityQueue<Pair<Int, Int>>(compareBy<Pair<Int, Int>> { it.second }.thenByDescending { it.first })

        for((k, v) in dict){
            pq.add(v to 0)
        }

        var timestamp = 0
        var ans = 0
        while(pq.size != 0){
            var cur = pq.peek()
            while (cur.second < timestamp){
                pq.poll()
                pq.add(cur.first to timestamp)
                cur = pq.peek()
            }
            if(cur.second == timestamp){
                if(cur.first != 1){
                    pq.add((cur.first - 1) to (timestamp + n + 1))
                }
                pq.poll()
            }
            ans++
            timestamp++
        }
        return ans
    }
}
