class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        int n = coins.size();
        vector <unsigned int> dp(amount+1);
        dp[0] = 0;
        for(int i = 1; i<=amount; i++){
            dp[i] = INT_MAX;
            for(auto x:coins){
                if(i>=x){
                    dp[i] = min(dp[i], dp[i-x]+1);
                }
            }
        }
        return (dp[amount] == INT_MAX ? -1:dp[amount]);
    }
};
