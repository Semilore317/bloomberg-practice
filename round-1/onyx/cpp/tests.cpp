#include <iostream>
#include <functional>
static int total=0, failures=0;
static void check(const char* n, bool c){ ++total; std::cout<<(c?"PASS ":(++failures,"FAIL "))<<n<<"\n"; }
static bool throws(std::function<void()> f){ try{ f(); return false; } catch(...) { return true; } }
#include "tokens.hpp"
int main(){
    { double t=1000; TokenStore s(60,[&]{return t;}); auto& x=s.issue("u1"); check("issued_token_validates", s.validate(x.token_id)); }
    { double t=1000; TokenStore s(60,[&]{return t;}); auto& x=s.issue("u1"); s.revoke(x.token_id); check("revoke_invalidates", s.validate(x.token_id)==false); }
    { double t=1000; TokenStore s(60,[&]{return t;}); auto& x=s.issue("u1"); t+=40; s.refresh(x.token_id); t+=40; check("refresh_extends_lifetime", s.validate(x.token_id)); }
    { double t=1000; TokenStore s(60,[&]{return t;}); check("unknown_token_invalid", s.validate("nope")==false); }
    { double t=1000; TokenStore s(60,[&]{return t;}); auto& x=s.issue("u1"); auto& r=s.refresh(x.token_id); check("refresh_returns_active", r.status==TokenStatus::ACTIVE); }
    { double t=1000; TokenStore s(60,[&]{return t;}); auto& x=s.issue("u1"); s.revoke(x.token_id); check("revoked_cannot_refresh", throws([&]{ s.refresh(x.token_id); })); }
    { double t=1000; TokenStore s(60,[&]{return t;}); auto& x=s.issue("u1"); s.revoke(x.token_id); check("double_revoke_rejected", throws([&]{ s.revoke(x.token_id); })); }
    { double t=1000; TokenStore s(60,[&]{return t;}); auto& x=s.issue("u1"); t+=61; check("expired_token_invalid", s.validate(x.token_id)==false); }
    { double t=1000; TokenStore s(60,[&]{return t;}); auto& x=s.issue("u1"); t+=61; check("expired_token_cannot_refresh", throws([&]{ s.refresh(x.token_id); })); }
    std::cout<<(failures?"FAILED ":"OK ")<<(total-failures)<<"/"<<total<<"\n"; return failures?1:0;
}
