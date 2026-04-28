class Solution {
public:
    int uniquePaths(int m, int n) {
        int dp[n+2][m+2];
        for(int i = 0; i<n+2; i++){
            for(int j = 0; j<m+2; j++){dp[i][j] = 0;}
        }
        dp[n+1][m] = 1;
        for(int i = n; i>0; i--){
            for(int j = m; j>0; j--){
                dp[i][j] = dp[i+1][j] + dp[i][j+1];
            }
        }
        return dp[1][1];
    }
};
