class Solution {
public:
    int search(vector<int>& nums, int target) {
        int ans = -1, l = 0, r = size(nums) - 1;
        while(ans == -1 && l <= r){
            int mid = (l + r) / 2;
            if(nums[mid] == target) ans = mid;
            else if(nums[mid] < target) l = mid + 1;
            else r = mid - 1;
        }
        return ans;
    }
};
