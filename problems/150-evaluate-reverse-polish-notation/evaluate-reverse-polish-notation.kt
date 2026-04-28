class Solution {
    fun evalRPN(tokens: Array<String>): Int {
        var stack = ArrayDeque<String>()

        for(token in tokens){
            var num = token.toIntOrNull();
            if(num == null){
                var r = stack.removeLast().toInt()
                var l = stack.removeLast().toInt()

                when(token) {
                    "+" -> num = l + r
                    "-" -> num = l - r
                    "*" -> num = l * r
                    "/" -> num = l / r   
                }
            } 
            stack.addLast(num.toString())
        }
        return stack.last().toIntOrNull() ?: 0
    }
}
