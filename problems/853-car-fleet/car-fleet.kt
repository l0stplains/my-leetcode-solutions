class Solution {
    fun carFleet(target: Int, position: IntArray, speed: IntArray): Int {
        val zipped = position.zip(speed).sortedByDescending {it.first} 
        var stack = ArrayDeque<Double>()

        for((p, s) in zipped){
            val tm = (target - p).toDouble() / s
            if(stack.isEmpty() || stack.last() < tm){
                stack.addLast(tm)
            }
            else {
                stack.addLast( maxOf(stack.removeLast(), tm))
            }
        }

        return stack.size

    }
}
