import java.util.*;
public class Orders {
    public enum OrderStatus { OPEN, PARTIAL, FILLED, CANCELLED }
    public static class Order {
        public String orderId, symbol, side; public int qty, filled; public OrderStatus status;
        Order(String id,String sym,String sd,int q){orderId=id;symbol=sym;side=sd;qty=q;filled=0;status=OrderStatus.OPEN;}
    }
    private final Map<String,Order> orders = new LinkedHashMap<>();
    private int seq = 0;
    public Order place(String symbol, String side, int qty){
        if(!side.equals("buy") && !side.equals("sell")) throw new IllegalArgumentException("side");
        if(qty<=0) throw new IllegalArgumentException("qty");
        String id="O"+(++seq); Order o=new Order(id,symbol,side,qty); orders.put(id,o); return o;
    }
    public Order fill(String id, int qty){
        Order o=get(id);
        if(qty<=0) throw new IllegalArgumentException("fill qty");
        o.filled+=qty;
        o.status = (o.filled==o.qty)?OrderStatus.FILLED:OrderStatus.PARTIAL;
        return o;
    }
    public Order cancel(String id){
        Order o=get(id);
        o.status=OrderStatus.CANCELLED; return o;
    }
    public int remaining(String id){ Order o=get(id); return o.qty-o.filled; }
    public int openQtyFor(String symbol){
        int s=0;
        for(Order o: orders.values()) if(o.symbol.equals(symbol)) s+=o.qty-o.filled;
        return s;
    }
    public Order get(String id){ Order o=orders.get(id); if(o==null) throw new IllegalArgumentException("not found"); return o; }
}
