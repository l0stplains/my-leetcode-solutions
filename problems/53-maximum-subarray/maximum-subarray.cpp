class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int maks = nums[0], cur = nums[0];
        for(int i = 1; i< size(nums); i++){
            int x = nums[i];
            cur = max(x, cur + x);
            maks = cur > maks ? cur : maks;
        }
        return maks;
    }
};
