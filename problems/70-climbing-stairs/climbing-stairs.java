class Solution {
    public int climbStairs(int n) {
        if (n < 3) return n;
        int a = 1;
        int b = 2;
        int ans = a + b;
        
        for(int i = 3; i < n; i++){
            a = b;
            b = ans;
            ans = a + b;
        }

        return ans;
    }
}
