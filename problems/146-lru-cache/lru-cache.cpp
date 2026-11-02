class LRUCache {
  unordered_map<int, int> store;
  unordered_map<int, pair<int, int>> link;
  int latest = -1;
  int newest = -1;
  int capacity;

public:
  LRUCache(int capacity) { this->capacity = capacity; }

  int get(int key) {
    if (store.count(key)) {
      int next = link[key].first;
      int prev = link[key].second;

      if (prev != -1) {

        if (next != -1) {
          link[next].second = prev;
        } else {
            latest = prev;
        }
        link[prev].first = next;

        link[newest].second = key;
        link[key].first = newest;
        link[key].second = -1;

        newest = key;
      }

      return store[key];
    }
    return -1;
  }

  void put(int key, int value) {
    if (store.count(key)) {
      int next = link[key].first;
      int prev = link[key].second;

      if (prev != -1) {

        if (next != -1) {
          link[next].second = prev;
        } else {
            latest = prev;
        }
        link[prev].first = next;

        link[newest].second = key;
        link[key].first = newest;
        link[key].second = -1;

        newest = key;
      }
    } else {
        if (store.size() == capacity){
            store.erase(latest);
            int prev = link[latest].second;
            if(prev != -1){
                link[prev].first = -1;
            }
            latest = prev;
        }

        if(newest != -1) {
            link[newest].second = key;
        }
        link[key].first = newest;
        link[key].second = -1;

        newest = key;


        if(latest == -1){
            latest = newest;
        }
    }

    store[key] = value;
  }
};



/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache* obj = new LRUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */
