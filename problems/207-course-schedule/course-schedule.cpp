class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        unordered_map<int, int> counter;
        unordered_map<int, unordered_set<int>> mp;


        for(int i = 0; i < prerequisites.size(); i++){
            counter[prerequisites[i][0]]++;
            mp[prerequisites[i][1]].insert(prerequisites[i][0]);
        }

        queue<int> q;

        for(int i = 0; i < numCourses; i++){
            if(!counter.count(i)) q.push(i);
        }

        while(!q.empty()){
            int cur = q.front();
            q.pop();

            for(int x : mp[cur]){
                counter[x]--;
                if(!counter[x]){
                    counter.erase(x);
                    q.push(x);
                }
            }
        }


        return counter.empty();

    }
};
