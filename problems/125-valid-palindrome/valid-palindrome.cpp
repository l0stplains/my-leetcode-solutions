class Solution {
public:
    bool isPalindrome(string s) {
        string filtered = "";

        for(auto c: s){
            if(c >= 'A' && c <= 'Z'){
                filtered += (char) (c + ((int) 'a' - 'A'));
            } else if (c >= 'a' && c <= 'z'){
                filtered += c;
            } else if(c >= '0' && c <= '9'){
                filtered += c;
            }
        }
        int l  = 0, r = filtered.length() - 1;
        while(l < r){
            if(filtered[l] != filtered[r]){
                return false;
            }
            l++;
            r--;
        }
        return true;
    }
};
