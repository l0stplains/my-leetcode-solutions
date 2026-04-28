class MyHashMap() {

    val map = IntArray(1000005) { -1 }

    fun put(key: Int, value: Int) {
        map[key] = value
    }

    fun get(key: Int): Int {
        return map[key]
    }

    fun remove(key: Int) {
        map[key] = -1
    }

}

/**
 * Your MyHashMap object will be instantiated and called as such:
 * var obj = MyHashMap()
 * obj.put(key,value)
 * var param_2 = obj.get(key)
 * obj.remove(key)
 */
