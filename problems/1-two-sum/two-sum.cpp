class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector <pair<int,int>> pr(nums.size());
        for(int i = 0; i<nums.size(); i++){
            pr[i] = make_pair(nums[i], i);
        }

        sort(pr.begin(), pr.end());

        int l = 0, r = nums.size() - 1;

        vector<int> ans;
        while(l != r){
            if(pr[l].first + pr[r].first == target){
                ans.push_back(pr[l].second);
                ans.push_back(pr[r].second);
                return ans;
            }
            if(pr[l].first + pr[r].first > target){
                r--;
            } else {
                l++;
            }
        }
        return ans;
    }
};
