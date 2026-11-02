class Solution {
public:
    void sortColors(vector<int>& nums) {
        vector<int> colorBucket(3, 0);
        for(auto x : nums){
            colorBucket[x]++;
        }

        int checkPoint = 0;
        for(int i = 0; i < 3; i++){
            int j;
            for( j = checkPoint; j - checkPoint < colorBucket[i]; j++){
                nums[j] = i;
            }
            checkPoint = j;
        }
    }
};
