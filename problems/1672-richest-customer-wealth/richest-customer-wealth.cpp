class Solution {
public:
    int maximumWealth(vector<vector<int>>& accounts) {
        int ans = 0;
        for(auto i : accounts){
            int wealth = 0;
            for(auto j : i){
                wealth += j;
            }
            ans = max(ans, wealth);
        }
        return ans;
    }
};
