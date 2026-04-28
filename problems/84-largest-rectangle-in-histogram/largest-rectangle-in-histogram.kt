class Solution {
    fun largestRectangleArea(heights: IntArray): Int {
        val n = heights.size
        val stackL = ArrayDeque<Pair<Int, Int>>()
        val stackR = ArrayDeque<Pair<Int, Int>>()
        data class Node(
            var left: Pair<Int, Int>,
            var right: Pair<Int, Int>
        )
        var arr = MutableList(n) {
            Node(0 to 0, 0 to 0)
        }


        stackL.addLast(-1 to -1)
        for((i, x) in heights.withIndex()){
            while (!stackL.isEmpty() && stackL.last().first >= x){
                stackL.removeLast()
            }

            arr[i].left = stackL.last()

            if(stackL.last().first < x){
                stackL.addLast(x to i)
            }
        }

        stackR.addLast(-1 to n)
        for (i in heights.lastIndex downTo 0) {
            val x = heights[i]
            while (!stackR.isEmpty() && stackR.last().first >= x){
                stackR.removeLast()
            }

            arr[i].right = stackR.last()

            if(stackR.last().first < x){
                stackR.addLast(x to i)
            }
        }

        var ans = 0;
        
        for((i, node) in arr.withIndex()){
            ans = maxOf(ans, heights[i] * (node.right.second - node.left.second - 1))
        }

        return ans
    }
}
