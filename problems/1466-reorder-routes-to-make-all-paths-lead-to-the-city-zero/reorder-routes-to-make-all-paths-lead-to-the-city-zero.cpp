class Solution {
public:
    int minReorder(int n, vector<vector<int>>& connections) {
        vector<vector<int>> ab(n);
        vector<vector<int>> ba(n);
        vector<bool> don(n, false);


        for(int i = 0; i < connections.size(); i++){
            ab[connections[i][0]].push_back(connections[i][1]);
            ba[connections[i][1]].push_back(connections[i][0]);
        }


        int ans = 0;
        queue<int> q;

        q.push(0);
        

        while(!q.empty()){
            int cur = q.front();
            q.pop();
            don[cur] = true;
            for(int x : ab[cur]){
                if(!don[x]){
                ans++;
                q.push(x);
                }
            }
            for(int x : ba[cur]){
                if(!don[x]){
                q.push(x);
                }
            }
        }
        return ans;
    }
};
