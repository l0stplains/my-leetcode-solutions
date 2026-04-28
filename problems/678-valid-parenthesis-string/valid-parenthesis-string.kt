class Solution {
    fun checkValidString(s: String): Boolean {
        val q = ArrayDeque<Int>()

        var fromLeft = true
        var curS = 0

        for(c in s){
            //print(c)
            if(c == '(') q.addLast(1)
            if(c == ')') {
                if(q.isEmpty()){
                    if(curS > 0){
                        curS--
                        continue
                    }
                    //println("wakwaw")
                    fromLeft = false
                    break
                }
                q.removeLast() 
            }
            if(c == '*') curS++
        }

        //println(q.size)
        //if(fromLeft) fromLeft = q.isEmpty()

        q.clear()
        //println(q.size)

        var fromRight = true
        curS = 0

        for (i in s.length - 1 downTo 0) {
            val c = s[i]
            //print(c)
            if(c == ')') q.addLast(1)
            if(c == '(') {
                if(q.isEmpty()){
                    if(curS > 0){
                        curS--
                        continue
                    }
                    //println("wakwawr")
                    fromRight = false
                    break
                }
                q.removeLast() 
            }
            if(c == '*') curS++
        }

        //println(q.size)
        //if(fromRight) fromRight = q.isEmpty()


        return fromRight && fromLeft

    }
}
