class Solution {
public:

    vector<int> asteroidCollision(vector<int>& asteroids) {
        stack<int> st;

        for(int a : asteroids){
            if(st.empty()){
                st.push(a);
                continue;
            }

            int top = st.top();
            bool store = true;
            while(a < 0 && top > 0){
                if(top > abs(a)){
                    store = false;
                    break;
                }
                st.pop();
                if(top == abs(a)){
                    store = false;
                    break;
                }
                if(st.empty()) break;
                top = st.top();
            }
            if(store) st.push(a);
        }

        vector<int> ans(st.size());

        for(int i = ans.size() - 1; i >= 0; i--){
            ans[i] = st.top();
            st.pop();
        }
        return ans;
    }
};
