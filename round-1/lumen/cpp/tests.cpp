#include <iostream>
#include <functional>
static int total=0, failures=0;
static void check(const char* n, bool c){ ++total; std::cout<<(c?"PASS ":(++failures,"FAIL "))<<n<<"\n"; }
static bool throws(std::function<void()> f){ try{ f(); return false; } catch(...) { return true; } }
#include "jobs.hpp"
int main(){
    { JobQueue q(2); auto& j=q.enqueue("p"); check("enqueue_queued", j.status==JobStatus::QUEUED); }
    { JobQueue q(2); auto& j=q.enqueue("p"); q.start(j.job_id); check("start_runs", q.status(j.job_id)==JobStatus::RUNNING && j.attempts==1); }
    { JobQueue q(2); auto& j=q.enqueue("p"); q.start(j.job_id); q.complete(j.job_id); check("complete_done", q.status(j.job_id)==JobStatus::DONE); }
    { JobQueue q(2); auto& j=q.enqueue("p"); q.start(j.job_id); q.fail(j.job_id); check("fail_requeues_under_budget", q.status(j.job_id)==JobStatus::QUEUED); }
    { JobQueue q(2); auto& j=q.enqueue("p"); q.start(j.job_id); q.fail(j.job_id); q.start(j.job_id); q.complete(j.job_id); check("retry_then_succeed", q.status(j.job_id)==JobStatus::DONE); }
    { JobQueue q(2); auto& j=q.enqueue("p"); q.start(j.job_id); q.fail(j.job_id); q.start(j.job_id); q.fail(j.job_id); check("fails_after_budget", q.status(j.job_id)==JobStatus::FAILED); }
    { JobQueue q(2); auto& j=q.enqueue("p"); q.start(j.job_id); check("start_requires_queued", throws([&]{ q.start(j.job_id); })); }
    { JobQueue q(2); auto& j=q.enqueue("p"); check("complete_requires_running", throws([&]{ q.complete(j.job_id); })); }
    { JobQueue q(2); check("unknown_job_raises", throws([&]{ q.start("nope"); })); }
    std::cout<<(failures?"FAILED ":"OK ")<<(total-failures)<<"/"<<total<<"\n"; return failures?1:0;
}
