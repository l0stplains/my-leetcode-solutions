class Solution(object):
    def merge(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        """

        intervals.sort(key=lambda x: (x[0], x[1]))

        cur = None

        result = []

        for x in intervals:
            if cur == None:
                cur = x
                continue
            if x[0] <= cur[1]:
                if x[1] > cur[1]:
                    cur[1] = x[1]
            else:
                result.append(cur)
                cur = x
        
        result.append(cur)

        return result
            
        
