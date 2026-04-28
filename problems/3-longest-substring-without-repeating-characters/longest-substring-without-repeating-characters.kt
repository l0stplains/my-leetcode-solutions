class Solution {
    fun lengthOfLongestSubstring(s: String): Int {

        val mp = mutableMapOf<Char, Int>()

        var l = 0
        
        var ans = 0
        for(r in 0..s.length - 1){
            while((mp[s[r]] ?: 0) != 0){
                mp[s[l]] = 0
                l++
            }
            mp[s[r]] = 1
            ans = maxOf(ans, r - l + 1)
        }

        return ans

    }
}
