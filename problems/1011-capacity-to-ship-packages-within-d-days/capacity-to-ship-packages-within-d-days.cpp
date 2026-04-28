class Solution {
public:

    int check(vector<int>& weights, int cap) {
        int res = 0;
        int temp = 0;
        for(int w : weights){
            if(temp < w) {
                res++;
                temp = cap;
                // cout << endl;
            }
            // cout << w << " ";
            temp -= w;
        }
        // cout << endl;
        return res;
    }
    int shipWithinDays(vector<int>& weights, int days) {

        int l = weights[0], r = 0;

        for(int x : weights){
            r+=x;
            l = max(l, x);
        }
        int ans = -1;
        while(l <= r){
            int m = (l + r) / 2;
            // cout << "l: " << l << " r: " << r << " m: " << m << endl;
            int day = check(weights, m);

            if(day > days){
                l = m + 1;
            } else if (day < days){
                ans = m;
                r = m - 1;
            } else {
                ans = m;
                r--;
            }
        }
        return ans;
    }
};
