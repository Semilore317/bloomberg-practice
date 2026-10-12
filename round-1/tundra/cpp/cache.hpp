#pragma once
#include <string>
#include <list>
#include <unordered_map>
#include <utility>
#include <functional>
struct Entry { int value; double expires_at; };
class LRUCache {
    int cap_; double ttl_; std::function<double()> clock_;
    std::list<std::pair<std::string, Entry>> order_;   // front = LRU, back = most recent
    std::unordered_map<std::string, std::list<std::pair<std::string, Entry>>::iterator> idx_;
public:
    LRUCache(int cap, double ttl, std::function<double()> clock): cap_(cap), ttl_(ttl), clock_(clock) {}
    void put(const std::string& key, int value){
        auto it = idx_.find(key);
        if(it != idx_.end()){ order_.erase(it->second); idx_.erase(it); }
        order_.push_back({key, Entry{value, clock_() + ttl_}});
        idx_[key] = std::prev(order_.end());
        while((int)order_.size() > cap_){
            idx_.erase(order_.front().first);
            order_.pop_front();                       // evict the front (least recently used)
        }
    }
    std::pair<bool,int> get(const std::string& key){
        auto it = idx_.find(key);
        if(it == idx_.end()) return {false, 0};
        // BUG: no expiry check, an expired entry is still returned
        // BUG: does not mark the key as recently used, so LRU order is wrong
        return {true, it->second->second.value};
    }
    int size(){
        // BUG: counts expired entries that have not been purged yet
        return (int)order_.size();
    }
};
