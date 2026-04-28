class Solution {
    fun isValid(s: String): Boolean {
        val stack = ArrayDeque<Char>()

        for(char in s){
            when (char) {
                '{', '[', '(' -> stack.addLast(char)
                '}' -> {
                     if (stack.isEmpty()) return false
                    val top = stack.removeLast()
                    if (!(top == '{')){
                        return false
                    }
                }
                ']' -> {
                     if (stack.isEmpty()) return false
                    val top = stack.removeLast()
                    if (!(top == '[')){
                        return false
                    }
                }
                ')' -> {
                     if (stack.isEmpty()) return false
                    val top = stack.removeLast()
                    if (!(top == '(')){
                        return false
                    }
                }
                else -> {
                    return false
                }
                
            }
        }
        return stack.isEmpty()
    }
}
