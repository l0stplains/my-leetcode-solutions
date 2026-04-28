class Solution {
public:
    int dp[46] = {0};
    int climbStairs(int n) {
        if(n<2) return 1;
        if(dp[n]) return dp[n];
        dp[n] = climbStairs(n-2) + climbStairs(n-1);
        return dp[n]; 
    }
};
