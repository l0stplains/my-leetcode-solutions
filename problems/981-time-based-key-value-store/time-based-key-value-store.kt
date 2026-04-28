class TimeMap() {
    val store = mutableMapOf<String, ArrayDeque<Pair<String, Int>>>()

    fun set(key: String, value: String, timestamp: Int) {
        store.getOrPut(key){ ArrayDeque() }.addLast(value to timestamp)
    }

    fun get(key: String, timestamp: Int): String {
        if(!(key in store)){
            return ""
        }

        var arr = store[key]!!

        var l = 0
        var r = arr.size - 1

        var m = 0
        while(l <= r){
            m = (l + r) / 2

            var cur = arr[m].second
            if ( cur == timestamp) {
                break
            } else if (cur < timestamp) {
                if (m != arr.size - 1 && arr[m + 1].second > timestamp){
                    break
                }
                l = m + 1
            } else {
                r = m - 1
            }
            
        }

        if (arr[m].second <= timestamp) return arr[m].first
        return ""
    }

}

/**
 * Your TimeMap object will be instantiated and called as such:
 * var obj = TimeMap()
 * obj.set(key,value,timestamp)
 * var param_2 = obj.get(key,timestamp)
 */
