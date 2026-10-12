#pragma once
#include <string>
#include <map>
#include <stdexcept>
enum class ConnStatus { IN_USE, IDLE };
struct Connection { std::string conn_id; ConnStatus status; };
class ConnectionPool {
    int capacity_; std::map<std::string,Connection> conns_; bool closed_=false; int seq_=0;
public:
    explicit ConnectionPool(int capacity): capacity_(capacity) {}
    Connection& acquire(){
        for(auto& kv:conns_) if(kv.second.status==ConnStatus::IDLE){ kv.second.status=ConnStatus::IN_USE; return kv.second; }
        std::string id="C"+std::to_string(++seq_);
        conns_[id]=Connection{id,ConnStatus::IN_USE}; return conns_[id];
    }
    Connection& release(const std::string& id){
        Connection& c=get(id);
        c.status=ConnStatus::IDLE; return c;
    }
    void close(){ closed_=true; }
    int in_use_count(){ int n=0; for(auto& kv:conns_) if(kv.second.status==ConnStatus::IN_USE) n++; return n; }
    int idle_count(){ int n=0; for(auto& kv:conns_) if(kv.second.status==ConnStatus::IDLE) n++; return n; }
    int size(){ return (int)conns_.size(); }
    Connection& get(const std::string& id){ auto it=conns_.find(id); if(it==conns_.end()) throw std::invalid_argument("connection not found"); return it->second; }
};
