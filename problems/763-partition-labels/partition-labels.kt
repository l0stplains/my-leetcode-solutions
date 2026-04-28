class Solution {
    fun partitionLabels(s: String): List<Int> {
        val last = mutableMapOf<Char, Int>()
        for(i in 0..s.length - 1){
            last[s[i]] = i
        }


        val list = mutableListOf<Int>()

        
        var i = 0
        

        while(i < s.length){
            var j = i
            var right = last[s[i]]!!
            while(j <= right){
                right = maxOf(right, last[s[j]]!!)
                j++
            }
            list.add(j - i)
            i = j
        }

        return list
    }
}
