#pragma once
#include <string>
#include <map>
#include <functional>
#include <stdexcept>
enum class TokenStatus { ACTIVE, REVOKED };
struct Token { std::string token_id, user_id; TokenStatus status; double expires_at; bool has_expiry; };
class TokenStore {
    std::map<std::string,Token> tokens_;
    double ttl_; std::function<double()> clock_; int seq_=0;
public:
    TokenStore(double ttl, std::function<double()> clock): ttl_(ttl), clock_(clock) {}
    Token& issue(const std::string& user){
        std::string id="T"+std::to_string(++seq_);
        tokens_[id]=Token{id,user,TokenStatus::ACTIVE,clock_()+ttl_,true}; return tokens_[id];
    }
    bool validate(const std::string& id){
        auto it=tokens_.find(id);
        if(it==tokens_.end()) return false;
        // BUG: ignores expiry, so an expired token still validates
        return it->second.status==TokenStatus::ACTIVE;
    }
    Token& refresh(const std::string& id){
        Token& t=get(id);
        if(t.status!=TokenStatus::ACTIVE) throw std::invalid_argument("cannot refresh a revoked token");
        // BUG: does not check expiry, so an expired token can be refreshed back to life
        t.expires_at=clock_()+ttl_; return t;
    }
    Token& revoke(const std::string& id){
        Token& t=get(id);
        // BUG: no terminal guard, a revoked token can be revoked again
        t.status=TokenStatus::REVOKED; t.has_expiry=false; return t;
    }
    Token& get(const std::string& id){ auto it=tokens_.find(id); if(it==tokens_.end()) throw std::invalid_argument("token not found"); return it->second; }
};
