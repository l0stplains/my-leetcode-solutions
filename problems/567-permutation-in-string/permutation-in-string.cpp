class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        vector<int> arr('z' - 'a' + 1, 0);
        vector<int> cor('z' - 'a' + 1, 0);

        int l = 0, r = s1.size() - 1;

        for(int i = 0; i < min(s1.size(), s2.size()); i++){
            arr[s2[i] - 'a']++;
        }

        for(char x : s1){
            cor[x - 'a']++;
        }


        while(r < s2.size()){
            bool tempans = true;
            for(int i = 0; i < arr.size(); i++){
                if(arr[i] != cor[i]){
                    tempans = false;
                    break;
                }
            }

            if(tempans) return true;

            arr[s2[l] - 'a']--;
            l++;
            r++;
            if(r < s2.size()) arr[s2[r] - 'a']++;
        }

        return false;
    }
};
