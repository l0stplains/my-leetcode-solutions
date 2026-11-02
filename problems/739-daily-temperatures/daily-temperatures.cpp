class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        stack<pair<int, int>> st;


        vector<int> ans(temperatures.size());

        for(int i = temperatures.size() - 1; i >= 0; i--){

            int idx = -1;
            while(!st.empty()){
                if(st.top().first > temperatures[i]) {
                    idx = st.top().second;
                    break;
                }
                st.pop();
            }

            if(idx == -1) ans[i] = 0;
            else ans[i] = idx - i;

            
            st.push(make_pair(temperatures[i], i));

        }

        return ans;
    }
};
