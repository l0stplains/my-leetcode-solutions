class Solution {
    fun mergeTriplets(triplets: Array<IntArray>, target: IntArray): Boolean {
        var foundA = false
        var foundB = false
        var foundC = false

        for(l in triplets){
            if(l[0] == target[0] && l[1] <= target[1] && l[2] <= target[2]) foundA = true
            if(l[1] == target[1] && l[0] <= target[0] && l[2] <= target[2]) foundB = true
            if(l[2] == target[2] && l[1] <= target[1] && l[0] <= target[0]) foundC = true
        }

        return foundA && foundB && foundC
    }
}
