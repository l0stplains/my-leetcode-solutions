class Solution {
    public int rob(int[] nums) {
        int[] arr = new int[nums.length];

        int ans = -1;
        for(int i = 0; i < arr.length; i++){
            arr[i] = nums[i];
            int a = (i > 1 ? arr[i - 2] : 0);
            int b = (i > 2 ? arr[i - 3] : 0);
            arr[i] += Math.max(a, b);

            ans = Math.max(ans, arr[i]);
        }

        return ans;
    }
}
