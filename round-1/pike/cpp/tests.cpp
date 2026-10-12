#include <iostream>
#include <functional>
static int total=0, failures=0;
static void check(const char* n, bool c){ ++total; std::cout<<(c?"PASS ":(++failures,"FAIL "))<<n<<"\n"; }
static bool throws(std::function<void()> f){ try{ f(); return false; } catch(...) { return true; } }
#include "approvals.hpp"
int main(){
    { ApprovalService s; auto& d=s.submit("spec"); check("submit_is_pending", d.status==DocStatus::PENDING); }
    { ApprovalService s; auto& d=s.submit("spec"); s.approve(d.doc_id); check("approve_pending", s.status(d.doc_id)==DocStatus::APPROVED); }
    { ApprovalService s; auto& d=s.submit("spec"); s.reject(d.doc_id); check("reject_pending", s.status(d.doc_id)==DocStatus::REJECTED); }
    { ApprovalService s; auto& d=s.submit("spec"); s.withdraw(d.doc_id); check("withdraw_pending", s.status(d.doc_id)==DocStatus::WITHDRAWN); }
    { ApprovalService s; auto& d=s.submit("spec"); s.reject(d.doc_id); bool a=throws([&]{ s.approve(d.doc_id); }); auto& d2=s.submit("spec2"); s.approve(d2.doc_id); bool b=throws([&]{ s.approve(d2.doc_id); }); check("approve_requires_pending", a && b); }
    { ApprovalService s; auto& d=s.submit("spec"); s.approve(d.doc_id); check("withdraw_requires_pending", throws([&]{ s.withdraw(d.doc_id); })); }
    { ApprovalService s; auto& d=s.submit("spec"); s.approve(d.doc_id); check("reject_requires_pending", throws([&]{ s.reject(d.doc_id); })); }
    { ApprovalService s; auto& a=s.submit("a"); s.submit("b"); s.submit("c"); s.approve(a.doc_id); check("pending_count_counts_only_pending", s.pending_count()==2); }
    { ApprovalService s; check("unknown_doc_raises", throws([&]{ s.approve("nope"); })); }
    std::cout<<(failures?"FAILED ":"OK ")<<(total-failures)<<"/"<<total<<"\n"; return failures?1:0;
}
