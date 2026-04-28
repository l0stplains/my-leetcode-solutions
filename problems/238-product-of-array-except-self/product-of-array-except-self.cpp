class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int zero = 0;
        int index;
        int res = 1;
        for(int i = 0; i<nums.size(); i++){
            if(nums[i] == zero){
                zero ++;     
                index = i;       
            } else {
                res *= nums[i];
            }
        }
        vector<int> ans(nums.size(), 0);
        if(zero > 1){
            return ans;
        } else if(zero == 1){
            ans[index] = res;
        } else{
            for(int i = 0; i<nums.size(); i++){
                ans[i] = res / nums[i];
            }
        }
        return ans;
    }
};
