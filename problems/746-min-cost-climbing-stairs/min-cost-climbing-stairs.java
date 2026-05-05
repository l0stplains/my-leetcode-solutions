class Solution {
    public int minCostClimbingStairs(int[] cost) {
        if(cost.length < 3) return Math.min(cost[0], cost[1]);



        int a = cost[0];
        int b = cost[1];
        int ans = Math.min(a, b) + cost[2];
        for(int i = 3; i < cost.length; i++){
            a = b;
            b = ans;
            ans = Math.min(a, b) + cost[i];
        }

        return Math.min(ans, b);
    }
}
