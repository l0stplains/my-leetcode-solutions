class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();


        int curSum = 0;
        int ans = 0;

        for(int x : nums){
            curSum += x;
            map.put(curSum, map.getOrDefault(curSum, 0) + 1);
        }

        curSum = 0;

        for(int i = 0; i < nums.length; i++){
            ans += map.getOrDefault(k + curSum, 0);
            curSum += nums[i];
            map.put(curSum, map.getOrDefault(curSum, 1) - 1);
        }
        return ans;
    }
}
