class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int ans = 0;

        int l = 0, r = 0;

        vector<bool> lookup(256, false);

        while(r < s.size()){

            if(lookup[s[r]]){
                while(l < r && lookup[s[r]]) {
                    lookup[s[l]] = false;
                    l++;
                }
            }

            lookup[s[r]] = true;
            ans = max(ans, r - l + 1);

            r++;
        }

        return ans;
    }
};
