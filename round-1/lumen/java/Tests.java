public class Tests {
    static int total=0, failures=0;
    static void check(String n, boolean c){ total++; if(c) System.out.println("PASS "+n); else { failures++; System.out.println("FAIL "+n);} }
    interface R { void run(); }
    static boolean throwsEx(R r){ try{ r.run(); return false; } catch(RuntimeException e){ return true; } }
    public static void main(String[] a){
        { Jobs q=new Jobs(2); Jobs.Job j=q.enqueue("p"); check("enqueue_queued", j.status==Jobs.JobStatus.QUEUED); }
        { Jobs q=new Jobs(2); Jobs.Job j=q.enqueue("p"); q.start(j.jobId); check("start_runs", q.status(j.jobId)==Jobs.JobStatus.RUNNING && j.attempts==1); }
        { Jobs q=new Jobs(2); Jobs.Job j=q.enqueue("p"); q.start(j.jobId); q.complete(j.jobId); check("complete_done", q.status(j.jobId)==Jobs.JobStatus.DONE); }
        { Jobs q=new Jobs(2); Jobs.Job j=q.enqueue("p"); q.start(j.jobId); q.fail(j.jobId); check("fail_requeues_under_budget", q.status(j.jobId)==Jobs.JobStatus.QUEUED); }
        { Jobs q=new Jobs(2); Jobs.Job j=q.enqueue("p"); q.start(j.jobId); q.fail(j.jobId); q.start(j.jobId); q.complete(j.jobId); check("retry_then_succeed", q.status(j.jobId)==Jobs.JobStatus.DONE); }
        { Jobs q=new Jobs(2); Jobs.Job j=q.enqueue("p"); q.start(j.jobId); q.fail(j.jobId); q.start(j.jobId); q.fail(j.jobId); check("fails_after_budget", q.status(j.jobId)==Jobs.JobStatus.FAILED); }
        { Jobs q=new Jobs(2); Jobs.Job j=q.enqueue("p"); q.start(j.jobId); check("start_requires_queued", throwsEx(()->q.start(j.jobId))); }
        { Jobs q=new Jobs(2); Jobs.Job j=q.enqueue("p"); check("complete_requires_running", throwsEx(()->q.complete(j.jobId))); }
        { Jobs q=new Jobs(2); check("unknown_job_raises", throwsEx(()->q.start("nope"))); }
        System.out.println((failures>0?"FAILED ":"OK ")+(total-failures)+"/"+total); System.exit(failures>0?1:0);
    }
}
