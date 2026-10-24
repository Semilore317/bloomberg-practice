#pragma once
#include <string>
#include <map>
#include <functional>
#include <stdexcept>
enum class ResStatus { HELD, COMMITTED, RELEASED };
struct Reservation { std::string reservation_id, sku; int qty; ResStatus status; double expires_at; bool has_expiry; };
class InventoryService {
    std::map<std::string,int> capacity_, available_;
    std::map<std::string,Reservation> res_;
    double ttl_; std::function<double()> clock_; int seq_=0;
public:
    InventoryService(std::map<std::string,int> stock, double ttl, std::function<double()> clock)
        : capacity_(stock), available_(stock), ttl_(ttl), clock_(clock) {}
    int available(const std::string& sku){ cleanup(); return available_.at(sku); }
    Reservation& reserve(const std::string& sku, int qty){
        cleanup();
        if(!available_.count(sku)) throw std::invalid_argument("unknown sku");
        if(qty<=0) throw std::invalid_argument("qty must be positive");
        if(available_[sku]<qty) throw std::invalid_argument("not enough stock");
        std::string id="R"+std::to_string(++seq_);
        res_[id]=Reservation{id,sku,qty,ResStatus::HELD,clock_()+ttl_,true};
        available_[sku]-=qty; return res_[id];
    }
    Reservation& commit(const std::string& id){
        Reservation& r=get(id);
        if(r.status!=ResStatus::HELD) throw std::invalid_argument("only held reservations can be committed");
        r.status=ResStatus::COMMITTED; r.has_expiry=false; return r;
    }
    Reservation& release(const std::string& id){
        Reservation& r=get(id);
        available_[r.sku]+=r.qty; r.status=ResStatus::RELEASED; r.has_expiry=false; return r;
    }
    int reserved_units(const std::string& sku){
        return capacity_.at(sku)-available_.at(sku);
    }
    Reservation& get(const std::string& id){ auto it=res_.find(id); if(it==res_.end()) throw std::invalid_argument("reservation not found"); return it->second; }
private:
    void cleanup(){ double now=clock_(); for(auto& kv:res_){ auto& r=kv.second; if(r.status==ResStatus::HELD && r.has_expiry && r.expires_at<=now){ available_[r.sku]+=r.qty; r.status=ResStatus::RELEASED; } } }
};
