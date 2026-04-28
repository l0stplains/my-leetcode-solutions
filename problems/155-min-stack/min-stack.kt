class MinStack() {
    private var stack = ArrayDeque<Pair<Int, Int>>()

    fun push(`val`: Int) {
        val mini = if (stack.isEmpty()) `val` else minOf(`val`, stack.last().second)
        stack.addLast(`val` to mini)
    }

    fun pop() {
        stack.removeLast()
    }

    fun top(): Int {
        return stack.last().first
    }

    fun getMin(): Int {
        return stack.last().second
    }

}

/**
 * Your MinStack object will be instantiated and called as such:
 * var obj = MinStack()
 * obj.push(`val`)
 * obj.pop()
 * var param_3 = obj.top()
 * var param_4 = obj.getMin()
 */
