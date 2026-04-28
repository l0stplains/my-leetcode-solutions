class Solution {
    fun dailyTemperatures(temperatures: IntArray): IntArray {
        var stack = ArrayDeque<Pair<Int, Int>>()
        val n = temperatures.size
        var ans = IntArray(n) {0}

        for((i, temp) in temperatures.withIndex()){
            
            var top = temp
            while (!stack.isEmpty() && top > stack.last().first){
                var cur = stack.removeLast()
                ans[cur.second] = i - cur.second
            }
            stack.addLast(temp to i)
        }
        return ans
    }
}
