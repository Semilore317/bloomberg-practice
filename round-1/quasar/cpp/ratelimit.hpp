#pragma once
#include <string>
#include <map>
#include <functional>
struct Window { double start; int count; };
class RateLimiter {
    int limit_; double window_; std::function<double()> clock_;
    std::map<std::string,Window> state_;
public:
    RateLimiter(int limit, double window, std::function<double()> clock): limit_(limit), window_(window), clock_(clock) {}
    bool allow(const std::string& key){
        double now=clock_();
        auto it=state_.find(key);
        // BUG: only starts a window when there is none, never rolls an elapsed one
        if(it==state_.end()){ state_[key]=Window{now,0}; it=state_.find(key); }
        Window& w=it->second;
        if(w.count<limit_){ w.count++; return true; }
        return false;
    }
    int remaining(const std::string& key){
        auto it=state_.find(key);
        // BUG: does not account for an elapsed window, so the count reads stale
        if(it==state_.end()) return limit_;
        return limit_ - it->second.count;
    }
    void reset(const std::string& key){
        // BUG: does not actually clear the key's window
        (void)key;
    }
};
