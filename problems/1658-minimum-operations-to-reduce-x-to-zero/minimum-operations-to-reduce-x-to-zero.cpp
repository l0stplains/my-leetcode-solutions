class Solution {
public:
    int minOperations(vector<int>& nums, int x) {
        int n = nums.size();
        vector<int> suml(n);
        vector<int> sumr(n);
        int ans = 1000000000;
        suml[0] = nums[0];
        sumr[n - 1] = nums[n - 1];
        if(suml[0] == x) return 1;
        if(sumr[n - 1] == x) return 1;

        
        for(int i = 1; i < n; i++){
            suml[i] = nums[i] + suml[i - 1];
            if(suml[i] == x) ans = min(ans, i + 1);
        } 
        for(int i = n - 2; i >= 0; i--){
            sumr[i] = nums[i] + sumr[i + 1];
            if(sumr[i] == x) ans = min(ans, n - i);
        }

        for(int i = 0; i < n; i++){
            int l = i + 1;
            int r = n - 1;
            int m = -1;
            bool found = false;

            int look = x - suml[i];
            if(look < 0) continue;
            if(look == 0) {
                ans = min(i + 1, ans);
                continue;
            }
            while(l <= r && !found){
                m = (l + r) / 2;
                if(sumr[m] > look) l = m + 1;
                else if (sumr[m] < look) r = m - 1;
                else {
                    found = true;
                }
            }
            if(found){
                ans = min(i + 1 + n - m, ans);
            }
        }
        if(ans == 1000000000) ans = -1;
        return ans;
    }
};
