class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());

        vector<vector<int>> ans;

        unordered_map <int, vector<int>> data;
        for(int i = 0; i<nums.size(); i++){
            data[nums[i]].push_back(i);
        }
        vector<int> temp(3);
        int x = 0;
        bool found = false;
        int beforel = -99999999;
        
        for(int l = 0; l < nums.size(); l++){
            if(nums[l] == beforel){
                continue;
            }
            beforel = nums[l];
            int beforer = -99999999;
            for(int r = nums.size() - 1; r > l; r--){
            if(nums[r] == beforer){
                continue;
            }
            beforer = nums[r];
            if(data[(nums[l] + nums[r]) * -1].size()){
                for(auto i : data[(nums[l] + nums[r]) * -1]){
                    if(i > l && i < r){
                        temp[0] = nums[l]; temp[1] = nums[i]; temp[2] = nums[r];
                        ans.push_back(temp);
                        break;
                    }
                }
            }
        }
        }
        
       
        
        return ans;
    }
};
