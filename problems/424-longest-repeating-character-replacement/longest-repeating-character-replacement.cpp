class Solution {
public:
    int characterReplacement(string s, int k) {
        vector<int> arr((int)('Z' - 'A' + 1), 0);

        
        int l = 0, ans = 0;

        int maks = 0;
        for(int i = 0; i < s.size(); i++){
            arr[s[i] - 'A']++;
            maks = max(arr[s[i] - 'A'], maks);

            while((i - l + 1) - maks > k){
                arr[s[l] - 'A']--;
                l++;
            }
            ans = max(ans, i - l + 1);
        }

        return ans;

    }
};
