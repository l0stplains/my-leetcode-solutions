class Solution {
    public int maxProfit(int[] prices) {
        int res = 0;
        int curMin = prices[0];
        int curMax = prices[0];
        int temp = 0;
        for(int x : prices){
            if (x > curMax) {
                curMax = x;
                temp = curMax - curMin;
            } else {
                res += temp;
                temp = 0;
                curMin = x;
                curMax = x;
            }
        }
        res += temp;
        return res;
    }
}
