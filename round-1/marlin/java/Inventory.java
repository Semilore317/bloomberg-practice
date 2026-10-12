import java.util.*;
import java.util.function.DoubleSupplier;
public class Inventory {
    public enum ResStatus { HELD, COMMITTED, RELEASED }
    public static class Reservation { public String reservationId, sku; public int qty; public ResStatus status; double expiresAt; boolean hasExpiry;
        Reservation(String id,String s,int q,double e){reservationId=id;sku=s;qty=q;status=ResStatus.HELD;expiresAt=e;hasExpiry=true;} }
    private final Map<String,Integer> capacity=new HashMap<>(), available=new HashMap<>();
    private final Map<String,Reservation> res=new LinkedHashMap<>();
    private final double ttl; private final DoubleSupplier clock; private int seq=0;
    public Inventory(Map<String,Integer> stock, double ttl, DoubleSupplier clock){ capacity.putAll(stock); available.putAll(stock); this.ttl=ttl; this.clock=clock; }
    public int available(String sku){ cleanup(); return available.get(sku); }
    public Reservation reserve(String sku,int qty){
        cleanup();
        if(!available.containsKey(sku)) throw new IllegalArgumentException("unknown sku");
        if(qty<=0) throw new IllegalArgumentException("qty");
        if(available.get(sku)<qty) throw new IllegalArgumentException("not enough stock");
        String id="R"+(++seq); Reservation r=new Reservation(id,sku,qty,clock.getAsDouble()+ttl); res.put(id,r); available.put(sku,available.get(sku)-qty); return r;
    }
    public Reservation commit(String id){
        Reservation r=get(id);
        if(r.status!=ResStatus.HELD) throw new IllegalArgumentException("only held");
        r.status=ResStatus.COMMITTED; r.hasExpiry=false; return r;
    }
    public Reservation release(String id){
        Reservation r=get(id);
        available.put(r.sku,available.get(r.sku)+r.qty); r.status=ResStatus.RELEASED; r.hasExpiry=false; return r;
    }
    public int reservedUnits(String sku){
        return capacity.get(sku)-available.get(sku);
    }
    public Reservation get(String id){ Reservation r=res.get(id); if(r==null) throw new IllegalArgumentException("not found"); return r; }
    private void cleanup(){ double now=clock.getAsDouble(); for(Reservation r: res.values()) if(r.status==ResStatus.HELD && r.hasExpiry && r.expiresAt<=now){ available.put(r.sku,available.get(r.sku)+r.qty); r.status=ResStatus.RELEASED; } }
}
