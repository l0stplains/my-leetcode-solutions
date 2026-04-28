class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        vector<string> temp;
        for(int i = 0; i<strs.size(); i++){
            string temps = strs[i];
            sort(temps.begin(), temps.end());
            temp.push_back(temps);
        }
        vector<vector<string>> ans;
        vector<string> sorted;
        // ans.push_back(strs[0]);
        for(int i = 0; i < strs.size(); i++){
            bool found = false;
            for(int j = 0; j < sorted.size(); j++){
                if(temp[i] == sorted[j]){
                    ans[j].push_back(strs[i]);
                    found = true;
                    break;
                }
            }
            if(!found){
                vector<string> temparr;
                temparr.push_back(strs[i]);
                ans.push_back(temparr);
                sorted.push_back(temp[i]);

            }
        }
        return ans;
    }
};
