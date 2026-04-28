/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    vector<vector<int>> pathSum(TreeNode* root, int targetSum) {
        vector<vector<int>> res = solve(root, targetSum, 0);
        for(auto& v : res){
            reverse(v.begin(), v.end());
        }
        return res;
    }

    vector<vector<int>> solve(TreeNode* root, int targetSum, int tempSum){

        if(root == nullptr){
            return {};
        }
        int total = tempSum + root->val;
        if(root->left == nullptr && root->right == nullptr && total == targetSum){
            return {{root->val}};
        }

        vector<vector<int>> lres = solve(root->left, targetSum, total);
        vector<vector<int>> rres = solve(root->right, targetSum, total);

        vector<vector<int>> curRes;
        for(auto v : lres){
            v.push_back(root->val);
            curRes.push_back(v);
        }
        for(auto v : rres){
            v.push_back(root->val);
            curRes.push_back(v);
        }

        return curRes;
    }
};
