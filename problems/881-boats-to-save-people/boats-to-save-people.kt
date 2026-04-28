class Solution {
    fun numRescueBoats(people: IntArray, limit: Int): Int {
        people.sort()
        val n = people.size
        var l = 0
        var r = n - 1

        var ans = 0

        while(l < r){
            if(people[r] + people[l] > limit){
                ans++
                r--
                continue
            }
            ans++
            r--
            l++
        }
        if(l == r) ans++

        return ans
    }
}
