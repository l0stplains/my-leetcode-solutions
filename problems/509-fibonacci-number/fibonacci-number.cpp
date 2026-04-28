class Solution {
public:
    int dp[31] = {0};
    int fib(int n) {
        if(n<2) return n;
        if(dp[n]) return dp[n];
        dp[n] = fib(n-2) + fib(n-1);
        return dp[n];
    }
};
