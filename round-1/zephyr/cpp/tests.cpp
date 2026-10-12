#include <iostream>
#include <functional>
static int total=0, failures=0;
static void check(const char* n, bool c){ ++total; std::cout<<(c?"PASS ":(++failures,"FAIL "))<<n<<"\n"; }
static bool throws(std::function<void()> f){ try{ f(); return false; } catch(...) { return true; } }
#include "subscriptions.hpp"
int main(){
    { double t=1000; SubscriptionService s(60,[&]{return t;}); auto& x=s.start_trial("u1"); check("trial_is_entitled", x.status==SubStatus::TRIAL && s.is_entitled(x.sub_id)); }
    { double t=1000; SubscriptionService s(60,[&]{return t;}); auto& x=s.start_trial("u1"); s.activate(x.sub_id); check("activate_makes_active", x.status==SubStatus::ACTIVE && s.is_entitled(x.sub_id)); }
    { double t=1000; SubscriptionService s(60,[&]{return t;}); auto& x=s.start_trial("u1"); s.activate(x.sub_id); s.suspend(x.sub_id); check("suspend_removes_entitlement", !s.is_entitled(x.sub_id)); }
    { double t=1000; SubscriptionService s(60,[&]{return t;}); auto& x=s.start_trial("u1"); s.activate(x.sub_id); s.suspend(x.sub_id); s.resume(x.sub_id); check("resume_restores_entitlement", s.is_entitled(x.sub_id)); }
    { double t=1000; SubscriptionService s(60,[&]{return t;}); auto& x=s.start_trial("u1"); s.activate(x.sub_id); s.cancel(x.sub_id); check("cancel_removes_entitlement", !s.is_entitled(x.sub_id)); }
    { double t=1000; SubscriptionService s(60,[&]{return t;}); auto& x=s.start_trial("u1"); s.cancel(x.sub_id); check("cancelled_cannot_be_reactivated", throws([&]{ s.activate(x.sub_id); })); }
    { double t=1000; SubscriptionService s(60,[&]{return t;}); auto& x=s.start_trial("u1"); s.cancel(x.sub_id); check("double_cancel_rejected", throws([&]{ s.cancel(x.sub_id); })); }
    { double t=1000; SubscriptionService s(60,[&]{return t;}); auto& x=s.start_trial("u1"); t+=61; check("expired_trial_not_entitled", !s.is_entitled(x.sub_id)); }
    { double t=1000; SubscriptionService s(60,[&]{return t;}); auto& x=s.start_trial("u1"); s.activate(x.sub_id); t+=1000; check("active_survives_trial_ttl", s.is_entitled(x.sub_id)); }
    { double t=1000; SubscriptionService s(60,[&]{return t;}); auto& x=s.start_trial("u1"); t+=61; check("expired_trial_cannot_be_activated", throws([&]{ s.activate(x.sub_id); })); }
    std::cout<<(failures?"FAILED ":"OK ")<<(total-failures)<<"/"<<total<<"\n"; return failures?1:0;
}
