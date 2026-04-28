class Solution {
    fun isNStraightHand(hand: IntArray, groupSize: Int): Boolean {
        if (hand.size % groupSize != 0) return false

        val cnt = mutableMapOf<Int, Int>()
        var mini = hand[0]
        val total = (hand.size.toDouble() / groupSize).toInt()

        for(c in hand){
            cnt[c] = cnt.getOrDefault(c, 0) + 1
            mini = minOf(mini, c)
        }

        var curV = mini 

        for(i in 1..total){
            while(!(curV in cnt)) curV++
            var temp = curV
            for(j in 1..groupSize){
                if(!(temp in cnt)) return false
                cnt[temp] = cnt[temp]!! - 1
                if(cnt[temp] == 0){
                    cnt.remove(temp)
                }
                temp++
            }
        }

        return true


    
    }
}
