class Solution {
public:
    bool isValid(string s) {
        string stack = "";
        for(auto x : s){
            if(x == '(' || x == '[' || x == '{'){
                stack += x;
                continue;
            } 
            if(stack.size() == 0){return false;}
            if(x == ')' && stack[stack.size()-1] == '('){
                stack.pop_back();
                continue;
            } 
            if(x == '}' && stack[stack.size()-1] == '{'){
                stack.pop_back();
                continue;
            } 
            if(x == ']' && stack[stack.size()-1] == '['){
                stack.pop_back();
                continue;
            } 
            return false;
            
        }
        return (stack.size() == 0);
    }
};
