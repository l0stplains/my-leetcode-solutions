class Solution {
public:
    bool isAnagram(string s, string t) {
        int maps[26] = {};
        int mapt[26] = {};

        for(auto &c : s){
            maps[(int) c - 'a']++;
        }
        for(auto &c : t){
            mapt[(int) c - 'a']++;
        }

        for(int i = 0; i<26; i++){
            if(maps[i] != mapt[i]){
                return false;
            }
        }
        return true;
    }
};
