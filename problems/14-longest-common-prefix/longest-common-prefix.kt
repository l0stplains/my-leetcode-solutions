class Solution {
    fun longestCommonPrefix(strs: Array<String>): String {
        var ans = ""

        for(i in 1..strs[0]!!.length){
            val temp = strs[0]!!.substring(0, i)
            var stop = false
            for(j in 1..strs.size - 1){
                if(strs[j].length < i || !strs[j].startsWith(temp) ){
                    stop = true
                    break
                }
            }
            if(stop) break
            ans = temp
        }

        return ans

    }
}
