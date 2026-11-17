class Solution {
public:
    bool isBipartite(vector<vector<int>>& graph) {
        vector<int> colored(110, 0);


        for(int n = 0; n < graph.size(); n++){
            if(colored[n]) continue;
            int cur = 1;

            queue<vector<int>> q;

            q.push(graph[n]);
            colored[n] = cur;
            cur = 2;
            while(!q.empty()){
                int sz = q.size();
                for(int i = 0; i < sz; i++){
                    vector<int> temp = q.front();
                    q.pop();

                    for(int x : temp){
                        if(colored[x]){
                            if(colored[x] != cur){
                                return false;
                            }
                        } else {
                            colored[x] = cur;
                            q.push(graph[x]);
                        }
                    }

                }

                if(cur == 2) {
                    cur = 1;
                } else {
                    cur = 2;
                }
            }



            

        }

        return true;



    }
};
