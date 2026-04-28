class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int l = 0, r = numbers.size() - 1;
        vector<int> ans(2);
        while(l < r){
            if(numbers[l] + numbers[r] == target){
                ans[0] = ++l;
                ans[1] = ++r;
                return ans;
            } if(numbers[l] + numbers[r] < target){
                l++;
            } else if(numbers[l] + numbers[r] > target){
                r--;
            }
        }
        return ans;
    }
};
