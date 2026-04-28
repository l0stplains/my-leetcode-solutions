class Solution {
public:
    bool isPalindrome(int x) {
        string s = to_string(x);
        bool ans = true; int l = s.length();
        for(int  i = 0; i<l/2; i++){
            if(s[i]!=s[l-i-1]) ans = false;
        }
        return ans;
    }
};
