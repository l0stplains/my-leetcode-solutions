class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_map<int, pair<int, int>> um;
        int maks = 0;
        for(int i = 0; i < nums.size(); i++){
            if(um[nums[i]].second){
                continue;
            } 
            um[nums[i]] = make_pair(nums[i], 1);

            if(um[nums[i] + 1].second){
                int cur = nums[i] + 1;
                while(um[cur].first != cur){
                    cur = um[cur].first;
                }
                um[um[cur].first].second += um[nums[i]].second;
                um[nums[i]] = make_pair(um[cur].first, um[um[cur].first].second);
            }

            if(um[nums[i] - 1].second){
                int cur = nums[i] - 1;
                while(um[cur].first != cur){
                    cur = um[cur].first;
                }
                um[um[cur].first].second += um[nums[i]].second;
                
                if(um[um[nums[i]].first].second){
                    um[um[nums[i]].first].second = um[um[cur].first].second;
                    um[um[cur].first].first = um[nums[i]].first;
                }
                um[nums[i]] = make_pair(um[cur].first, um[um[cur].first].second);
            }
            maks = max(maks, um[nums[i]].second);
        }
        return maks;
        
    }
};
