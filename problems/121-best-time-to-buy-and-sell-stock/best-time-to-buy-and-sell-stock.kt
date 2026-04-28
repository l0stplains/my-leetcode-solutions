class Solution {
    fun maxProfit(prices: IntArray): Int {
        var l = prices[0]
        
        var ans = 0

        for(x in prices){
            l = minOf(l, x)
            ans = maxOf(ans, x - l)
            
        }

        return ans


    }
}
