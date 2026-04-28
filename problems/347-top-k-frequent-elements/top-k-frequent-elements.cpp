class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        map<int, int> mp;
        for(auto &x : nums){
            mp[x]++;
        }
        vector<int> ans(k);
        
        priority_queue<pair<int, int>> pq;

        for(auto x: mp){
            if(x.second){
                pq.push(make_pair(x.second, x.first));
            }
        }
        for(int i = 0; i < k; i++){
            ans[i] = pq.top().second;
            pq.pop();
        }
        return ans;
    }
};
