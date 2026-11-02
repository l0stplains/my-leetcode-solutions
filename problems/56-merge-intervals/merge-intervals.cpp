class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end());

        vector<vector<int>> ans;


        for(int i = 0; i < intervals.size(); i++){
            vector<int> cur = intervals[i];

            int end = cur[1];

            int j = i + 1;
            while(j < intervals.size() && intervals[j][0] <= end){
                end = max(end, intervals[j][1]);
                j++;
            }

            i = j -1;

            ans.push_back({cur[0], end});
        }

        return ans;
    }
};
