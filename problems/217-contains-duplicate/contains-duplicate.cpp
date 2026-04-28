class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_map <int, int> um;
        for(auto &x : nums){
            if(um[x] == 1){
                return true;
            } um[x] = 1;
        }
        return false;
    }
};
