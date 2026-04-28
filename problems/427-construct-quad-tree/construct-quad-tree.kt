/**
 * Definition for a QuadTree node.
 * class Node(var `val`: Boolean, var isLeaf: Boolean) {
 *     var topLeft: Node? = null
 *     var topRight: Node? = null
 *     var bottomLeft: Node? = null
 *     var bottomRight: Node? = null
 * }
 */

class Solution {


    fun getLeaf(grid: Array<IntArray>, x: Int, y: Int, n: Int): Int?{
        var cur: Int? = grid[y][x]
        for(i in y..y+n-1){
            for(j in x..x+n-1){
                if(grid[i][j] != cur!!){
                    cur = null
                    break
                }
            }
            if(cur == null) break
        }
        return cur
    }



    fun construct(grid: Array<IntArray>): Node? {
        return _construct(grid, 0, 0, grid.size)
    }

    fun _construct(grid: Array<IntArray>, x: Int, y: Int, n: Int): Node? {
        val cur = getLeaf(grid, x, y, n)
        if(cur != null) return Node(cur == 1, true)

        val node = Node(true, false)
        node.topLeft = _construct(grid, x, y, n / 2)
        node.topRight = _construct(grid, x + n / 2,y , n / 2)
        node.bottomLeft = _construct(grid, x, y + n / 2, n / 2)
        node.bottomRight = _construct(grid, x + n / 2, y + n / 2, n / 2)

        return node
    }
}
