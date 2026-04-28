class Solution {
    fun searchMatrix(matrix: Array<IntArray>, target: Int): Boolean {
        var l = 0
        var r = matrix.size - 1

        var i = 0
        while (l <= r){
            
            i = (r + l) / 2
            var cur = matrix[i][0]
            var next = if(i < matrix.size - 1) matrix[i + 1][0] else target + 1
            when {
                cur == target || next == target -> { return true }
                cur < target && next > target -> { break }
                cur < target -> { l = i + 1 }
                cur > target -> { r = i - 1 }
            }
            
        }

        l = 0
        r = matrix[i].size - 1

        var x = 0
        while (l <= r){
            x = (r + l) / 2
            var cur = matrix[i][x]

            when {
                cur < target -> { l = x + 1 }
                cur > target -> { r = x - 1 }
                cur == target -> { return true }
            }
        }

        return false
    }
}
