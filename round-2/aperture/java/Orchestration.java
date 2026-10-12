import java.util.*;
public class Orchestration {
    int maxRetries;
    List<String> ready = new ArrayList<>();
    Map<String,Integer> attempts = new HashMap<>();
    List<String> dead = new ArrayList<>();
    public Orchestration(int mr) { maxRetries = mr; }
    public void enqueue(String j) { attempts.put(j, 0); ready.add(j); }
    public String dequeue() { if (ready.isEmpty()) return null; return ready.get(0); }
    public void ack(String j) {}
    public void nack(String j) {
        ready.remove(j);
        if (attempts.get(j) > maxRetries) dead.add(j);
        else ready.add(j);
    }
    public List<String> deadLetters() { return dead; }
}
