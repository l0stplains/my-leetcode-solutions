class Solution {
    fun minEatingSpeed(piles: IntArray, h: Int): Int {
        var r: Long = piles[0].toLong()
        var l: Long = 1

        for(x in piles){
            r = maxOf(r, x.toLong())
        }


        var mid: Long = 0
        var maks = r
        var curSum: Long = 0
        while(l < r){
            mid = (r + l) / 2

            curSum = 0
            for(x in piles){
                curSum += (x + mid - 1) / mid
            }

            println(" curSum $curSum, l $l, r $r, mid $mid")
            when {
                curSum > h -> { l = mid + 1 }
                curSum <= h -> { r = mid }
            }
        }

        curSum = 0
        for(x in piles){
            curSum += (x + l - 1) / l
        }

        println("curSum $curSum, l $l r $r")
        return if (l <= maks && curSum <= h) l.toInt() else -1

    }
}
