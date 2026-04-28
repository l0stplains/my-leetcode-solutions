class MedianFinder() {
    val left = PriorityQueue<Int>(compareByDescending {it})
    val right = PriorityQueue<Int>()

    var nowLeft = true

    fun addNum(num: Int) {
        if(left.size == 0){
            left.add(num)
            return
        }
        if(num > left.peek()){
            if(right.size == left.size){
                right.add(num)
                left.add(right.poll())
            } else {
                right.add(num)
            }
        } else {
            if(left.size > right.size){
                
                left.add(num)
                right.add(left.poll())
                
            } else {
                left.add(num)
            }
        }

    }

    fun findMedian(): Double {
        if(left.size == right.size){
            return (left.peek() + right.peek()).toDouble() / 2 
        }
        return left.peek().toDouble()
    }

}

/**
 * Your MedianFinder object will be instantiated and called as such:
 * var obj = MedianFinder()
 * obj.addNum(num)
 * var param_2 = obj.findMedian()
 */
