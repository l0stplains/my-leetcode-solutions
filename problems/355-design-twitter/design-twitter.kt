class Twitter() {

    private var globalCounter = 0
    private var tweetStore = mutableMapOf<Int, ArrayDeque<Pair<Int, Int>>>()
    private var followDict: MutableMap<Int, MutableMap<Int, Boolean>> = mutableMapOf()

    fun postTweet(userId: Int, tweetId: Int) {
        tweetStore.getOrPut(userId) { ArrayDeque() }.addLast(tweetId to globalCounter)
        globalCounter++
    }

    fun getNewsFeed(userId: Int): List<Int> {
        val minHeap = PriorityQueue<Pair<Int, Int>>(compareBy {it.second})
        val following = followDict.getOrPut(userId) { mutableMapOf(userId to true) }
        for((id, bool) in following){
            if(!bool) continue
            val posts = tweetStore.getOrPut(id) {ArrayDeque()}
            for(i in posts.size - 1 downTo 0){
                if(minHeap.size < 10) minHeap.add(posts[i])
                else {
                    val cur = minHeap.poll()
                    if(cur.second > posts[i].second) {
                        minHeap.add(cur)
                        break
                    }

                    minHeap.add(posts[i])
                }
            }
        }

        val ans = ArrayDeque<Int>()

        while(minHeap.size != 0){
            val cur = minHeap.poll()
            ans.addFirst(cur.first)
        }

        return ans.toList()

    }

    fun follow(followerId: Int, followeeId: Int) {
        followDict.getOrPut(followerId) { mutableMapOf(followerId to true) }[followeeId] = true
    }

    fun unfollow(followerId: Int, followeeId: Int) {
        followDict.getOrPut(followerId) { mutableMapOf(followerId to true) }[followeeId] = false
    }

}

/**
 * Your Twitter object will be instantiated and called as such:
 * var obj = Twitter()
 * obj.postTweet(userId,tweetId)
 * var param_2 = obj.getNewsFeed(userId)
 * obj.follow(followerId,followeeId)
 * obj.unfollow(followerId,followeeId)
 */
