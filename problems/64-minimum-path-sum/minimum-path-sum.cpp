class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        int n = grid.size(), m = grid[0].size();
        int dp[n+2][m+2];
        for(int i = 0; i<n+2; i++){
            for(int j = 0; j<m+2; j++){dp[i][j] = 1e9;}
        }
        dp[n][m+1] = 0;
        for(int i = n; i>0; i--){
            for(int j = m; j>0; j--){
                dp[i][j] = min(dp[i][j+1], dp[i+1][j]) + grid[i-1][j-1];
            }
        }
        return dp[1][1];
    }
};
