class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        vector<vector<bool>> marked(grid.size(), vector<bool> (grid[0].size(), false));


        int ans = 0;
        for (int i = 0; i < grid.size(); i++){
            for(int j = 0; j < grid[i].size(); j++){

                if(marked[i][j] || grid[i][j] == '0') continue;

                queue<pair<int, int>> q;

                q.push({i, j});
                marked[i][j] = true;
                ans++;


                while(!q.empty()){
                    pair<int, int> cur = q.front(); 
                   
                    q.pop();
                    int x = cur.first, y = cur.second;

                    if(x != 0 && !marked[x-1][y] && grid[x-1][y] == '1') {
                        q.push({x - 1, y});
                        marked[x-1][y] = true;
                    }
                    if(y != 0 && !marked[x][y-1] && grid[x][y-1] == '1') {
                        q.push({x, y - 1});
                        marked[x][y - 1] = true;
                    }
                    if(x != grid.size()-1 && !marked[x+1][y] && grid[x+1][y] == '1') {
                        q.push({x + 1, y});
                        marked[x+1][y] = true;
                    }
                    if(y != grid[i].size()-1 && !marked[x][y+1] && grid[x][y+1] == '1') {
                        q.push({x, y + 1});
                        marked[x][y + 1] = true;
                    }

                    
                }

                
            }
        }

        return ans;
    }
};
