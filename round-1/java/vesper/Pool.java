import java.util.*;
public class Pool {
    public enum ConnStatus { IN_USE, IDLE }
    public static class Connection { public String connId; public ConnStatus status; Connection(String id){connId=id;status=ConnStatus.IN_USE;} }
    private final int capacity; private final Map<String,Connection> conns=new LinkedHashMap<>(); private boolean closed=false; private int seq=0;
    public Pool(int capacity){ this.capacity=capacity; }
    public Connection acquire(){
        for(Connection c: conns.values()) if(c.status==ConnStatus.IDLE){ c.status=ConnStatus.IN_USE; return c; }
        String id="C"+(++seq); Connection c=new Connection(id); conns.put(id,c); return c;
    }
    public Connection release(String id){
        Connection c=get(id);
        c.status=ConnStatus.IDLE; return c;
    }
    public void close(){ closed=true; }
    public int inUseCount(){ int n=0; for(Connection c: conns.values()) if(c.status==ConnStatus.IN_USE) n++; return n; }
    public int idleCount(){ int n=0; for(Connection c: conns.values()) if(c.status==ConnStatus.IDLE) n++; return n; }
    public int size(){ return conns.size(); }
    public Connection get(String id){ Connection c=conns.get(id); if(c==null) throw new IllegalArgumentException("connection not found"); return c; }
}
