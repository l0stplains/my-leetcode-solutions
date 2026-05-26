func exist(board [][]byte, word string) bool {
    rows, cols := len(board), len(board[0])

    mark := make([][]bool, rows)
    for i := range mark {
        mark[i] = make([]bool, cols)
    }

    var dfs func(i, x, y int) bool

    dfs = func(i, x, y int) bool {
        if i == len(word) {
            return true
        }

        if y < 0 || y >= rows || x < 0 || x >= cols {
            return false
        }

        if mark[y][x] {
            return false
        }

        if board[y][x] != word[i] {
            return false
        }

        mark[y][x] = true

        found := dfs(i+1, x-1, y) ||
            dfs(i+1, x+1, y) ||
            dfs(i+1, x, y-1) ||
            dfs(i+1, x, y+1)

        mark[y][x] = false

        return found
    }

    for y := 0; y < rows; y++ {
        for x := 0; x < cols; x++ {
            if dfs(0, x, y) {
                return true
            }
        }
    }

    return false
}
