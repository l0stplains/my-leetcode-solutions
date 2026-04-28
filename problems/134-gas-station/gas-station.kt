class Solution {
    fun canCompleteCircuit(gas: IntArray, cost: IntArray): Int {
        var ans = -1

        var i = 0
        val n = gas.size
        while(i < n){
            if(gas[i] >= cost[i]){
                var curGas = gas[i] - cost[i]
                val temp = i
                i = (i + 1) % n
                while(i != temp){
                    curGas += gas[i] - cost[i]
                    if(curGas < 0) break
                    i = (i + 1) % n
                }
                
                if(i == temp) {
                    
                    ans = i
                    break
                }
                if (i < temp) {
                    break
                } 
            }
            i++
        }
        return ans
    }
}
