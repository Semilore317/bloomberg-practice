public class Tests {
    static int total=0, failures=0;
    static void check(String n, boolean c){ total++; if(c) System.out.println("PASS "+n); else { failures++; System.out.println("FAIL "+n);} }
    interface R { void run(); }
    static boolean throwsEx(R r){ try{ r.run(); return false; } catch(RuntimeException e){ return true; } }
    public static void main(String[] a){
        { Approvals s=new Approvals(); Approvals.Document d=s.submit("spec"); check("submit_is_pending", d.status==Approvals.DocStatus.PENDING); }
        { Approvals s=new Approvals(); Approvals.Document d=s.submit("spec"); s.approve(d.docId); check("approve_pending", s.status(d.docId)==Approvals.DocStatus.APPROVED); }
        { Approvals s=new Approvals(); Approvals.Document d=s.submit("spec"); s.reject(d.docId); check("reject_pending", s.status(d.docId)==Approvals.DocStatus.REJECTED); }
        { Approvals s=new Approvals(); Approvals.Document d=s.submit("spec"); s.withdraw(d.docId); check("withdraw_pending", s.status(d.docId)==Approvals.DocStatus.WITHDRAWN); }
        { Approvals s=new Approvals(); Approvals.Document d=s.submit("spec"); s.reject(d.docId); boolean x=throwsEx(()->s.approve(d.docId)); Approvals.Document d2=s.submit("spec2"); s.approve(d2.docId); boolean y=throwsEx(()->s.approve(d2.docId)); check("approve_requires_pending", x && y); }
        { Approvals s=new Approvals(); Approvals.Document d=s.submit("spec"); s.approve(d.docId); check("withdraw_requires_pending", throwsEx(()->s.withdraw(d.docId))); }
        { Approvals s=new Approvals(); Approvals.Document d=s.submit("spec"); s.approve(d.docId); check("reject_requires_pending", throwsEx(()->s.reject(d.docId))); }
        { Approvals s=new Approvals(); Approvals.Document d=s.submit("a"); s.submit("b"); s.submit("c"); s.approve(d.docId); check("pending_count_counts_only_pending", s.pendingCount()==2); }
        { Approvals s=new Approvals(); check("unknown_doc_raises", throwsEx(()->s.approve("nope"))); }
        System.out.println((failures>0?"FAILED ":"OK ")+(total-failures)+"/"+total); System.exit(failures>0?1:0);
    }
}
