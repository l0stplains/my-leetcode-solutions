class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        unordered_map<int, int> sums;

        int sum = 0;
        for(int i = 0; i < nums.size(); i++){
            sum += nums[i];
            sums[sum]++;
        }

        int ans = 0;

        sum = 0;
        for(int i = 0; i < nums.size(); i++){
            sum += nums[i];
            ans += sums[sum + k - nums[i]];
            
            if(sums.count(sum)){
                sums[sum]--;
            }
            
        }

        return ans;
    }
    
};
