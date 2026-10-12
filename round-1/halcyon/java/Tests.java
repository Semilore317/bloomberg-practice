public class Tests {
    static int total=0, failures=0;
    static void check(String n, boolean c){ total++; if(c) System.out.println("PASS "+n); else { failures++; System.out.println("FAIL "+n);} }
    interface R { void run(); }
    static boolean throwsEx(R r){ try{ r.run(); return false; } catch(RuntimeException e){ return true; } }
    public static void main(String[] a){
        { Orders s=new Orders(); Orders.Order o=s.place("AAPL","buy",10); check("place_creates_open_order", o.status==Orders.OrderStatus.OPEN && s.remaining(o.orderId)==10); }
        { Orders s=new Orders(); Orders.Order o=s.place("AAPL","buy",10); s.fill(o.orderId,4); check("partial_fill_sets_partial_and_remaining", o.status==Orders.OrderStatus.PARTIAL && s.remaining(o.orderId)==6); }
        { Orders s=new Orders(); Orders.Order o=s.place("AAPL","buy",10); s.fill(o.orderId,10); check("full_fill_sets_filled", o.status==Orders.OrderStatus.FILLED && s.remaining(o.orderId)==0); }
        { Orders s=new Orders(); Orders.Order o=s.place("AAPL","buy",10); s.fill(o.orderId,4); s.fill(o.orderId,6); check("two_fills_accumulate", o.status==Orders.OrderStatus.FILLED); }
        { Orders s=new Orders(); Orders.Order o=s.place("AAPL","buy",10); check("overfill_rejected", throwsEx(()->s.fill(o.orderId,11))); }
        { Orders s=new Orders(); Orders.Order o=s.place("AAPL","buy",10); s.cancel(o.orderId); check("fill_cancelled_order_rejected", throwsEx(()->s.fill(o.orderId,1))); }
        { Orders s=new Orders(); Orders.Order o=s.place("AAPL","buy",10); s.cancel(o.orderId); check("cancel_open_order", o.status==Orders.OrderStatus.CANCELLED); }
        { Orders s=new Orders(); Orders.Order o=s.place("AAPL","buy",10); s.cancel(o.orderId); check("double_cancel_rejected", throwsEx(()->s.cancel(o.orderId))); }
        { Orders s=new Orders(); Orders.Order o=s.place("AAPL","buy",10); s.cancel(o.orderId); check("open_qty_excludes_cancelled", s.openQtyFor("AAPL")==0); }
        { Orders s=new Orders(); Orders.Order x=s.place("AAPL","buy",10); s.place("AAPL","buy",5); s.fill(x.orderId,4); check("open_qty_sums_remaining", s.openQtyFor("AAPL")==11); }
        System.out.println((failures>0?"FAILED ":"OK ")+(total-failures)+"/"+total); System.exit(failures>0?1:0);
    }
}
