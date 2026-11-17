class Solution {
public:
    vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {
        unordered_map<string, vector<string>> graph;
        unordered_map<string, string> name;

        for (const auto& account : accounts) {
            const string& first = account[1];

            for (int i = 1; i < account.size(); i++) {
                const string& email = account[i];

                graph[email];
                if (i > 1) {
                    graph[first].push_back(email);
                    graph[email].push_back(first);
                }

                name[email] = account[0];
            }
        }

        unordered_set<string> visited;
        vector<vector<string>> ans;

        for (const auto& [email, neighbors] : graph) {
            if (visited.count(email)) continue;

            queue<string> q;
            vector<string> merged;

            q.push(email);
            visited.insert(email);

            while (!q.empty()) {
                string cur = q.front();
                q.pop();

                merged.push_back(cur);

                for (const string& next : graph.at(cur)) {
                    if (visited.insert(next).second) {
                        q.push(next);
                    }
                }
            }

            sort(merged.begin(), merged.end());

            vector<string> result;
            result.push_back(name.at(email));
            result.insert(result.end(), merged.begin(), merged.end());

            ans.push_back(move(result));
        }

        return ans;
    }
};
