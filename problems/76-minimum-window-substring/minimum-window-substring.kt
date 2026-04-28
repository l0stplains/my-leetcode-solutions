class Solution {
    fun minWindow(s: String, t: String): String {
        val map = mutableMapOf<Char, ArrayDeque<Int>>()
        val cnt = mutableMapOf<Char, Int>()

        for(c in t){
            cnt[c] = (cnt[c] ?: 0) + 1
        }

        var ansMatch = 0
        for((k, v) in cnt){
            if(v > 0){
                ansMatch++
            }
        }

        /*
            YOO, DON'T JUDGE MY CODE AHAHAHHA
            I JUST STARTED LEARNING KOTLIN AND IM FRUSTRATED WITH IT SO I JUST TYPE ANYTHING
         */

        var curMatch = 0

        var ans = Int.MAX_VALUE
        var idxAns = -1

        var last: Char? = null
        for(i in 0..s.length - 1){
            var cur = s[i]

            if(cur in cnt){
                if(last == null) {
                    last = cur
                    map.getOrPut(cur) { ArrayDeque() }.addLast(i)
                    if(map.getOrPut(cur) { ArrayDeque() }.size == cnt.getOrPut(cur) { 0 }) curMatch++
                    
                }
                
                else {
                    // println("i: $i")
                    map.getOrPut(cur) { ArrayDeque() }.addLast(i)
                    if(map.getOrPut(cur) { ArrayDeque() }.size == cnt.getOrPut(cur) { 0 }) curMatch++
                    
                    // println("curmatch: $curMatch, ansMatch: $ansMatch")
                    while(map.getOrPut(last ?: '1') { ArrayDeque() }.size > cnt.getOrPut(last ?: '1') { 0 }){
                        var curIdx = map.getOrPut(last ?: '1') { ArrayDeque() }.removeFirst()
                        // println("curidx: $curIdx")
                        
                        if (map.getOrPut(last ?: '1') { ArrayDeque() }.size + 1 == cnt.getOrPut(last ?: '1') { 0 }) curMatch--
                        // println("xx curmatch: $curMatch, ansMatch: $ansMatch")
                        // println("szz = ${map.getOrPut(last ?: '1') { ArrayDeque() }.size} should be ${cnt.getOrPut(cur) { 0 }}")
                        curIdx++
                        while(curIdx < s.length){
                            if(s[curIdx] in cnt){
                                // print("curidx: $curIdx, last: $s[curIdx]")
                                last = s[curIdx]
                                break
                            }
                            curIdx++
                        }
                    }
                }

                

                if (curMatch == ansMatch){
                    
                    var idx = map.getOrPut(last ?: '1') { ArrayDeque() }.first()
                    var tempo = i - idx + 1
                    // println("${last ?: '0'} i: $i idx: $idx, tempo: $tempo")
                    if(tempo < ans){
                        ans = tempo
                        idxAns = idx
                    }
                }
            }

        }

        if(idxAns == -1){
            return ""
        } else {
            return s.substring(idxAns, idxAns + ans)
        }
    }
}
