class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {

        int m = grid.size();
        int n = grid[0].size();
        
        queue<pair<int, int>> q;

        int freshCounter = 0;

        for(int i = 0; i < m; i++){
            for(int j = 0; j < n; j++){
                if(grid[i][j] == 1) freshCounter++;
                if(grid[i][j] == 2) q.push(make_pair(i, j)); 
            }
        }

        int cnt = -1;
        if(freshCounter == 0) return 0;

        while(!q.empty()){
            int qsize = q.size();
            for(int i = 0; i < qsize; i++){
                pair<int, int> cur = q.front();
                q.pop();
                int x = cur.first, y = cur.second;

                if(x != 0 && grid[x - 1][y] == 1){
                    freshCounter--;
                    grid[x - 1][y] = 2;
                    q.push(make_pair(x - 1, y));
                }
                if(y != 0 && grid[x][y - 1] == 1){
                    freshCounter--;
                    grid[x][y - 1] = 2;
                    q.push(make_pair(x, y - 1));
                }
                if(x != m - 1 && grid[x + 1][y] == 1){
                    freshCounter--;
                    grid[x + 1][y] = 2;
                    q.push(make_pair(x + 1, y));
                }
                if(y != n - 1 && grid[x][y + 1] == 1){
                    freshCounter--;
                    grid[x][y + 1] = 2;
                    q.push(make_pair(x, y + 1));
                }
            }
            cnt++;
        }
        if(freshCounter == 0) return cnt;
        else return -1;
    }
};
