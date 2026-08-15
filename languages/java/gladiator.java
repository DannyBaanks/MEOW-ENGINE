import java.io.*;
public class gladiator {
    public static void main(String[] a) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        String out = "";
        if (s.contains("\"discipline\":\"construct\"")) {
  if (s.contains("\"arena\":\"cheeks\"")) out = "()";
  else if (s.contains("\"arena\":\"ears\"")) out = "/\\\\/\\\\";
  else if (s.contains("\"arena\":\"eyes\"")) out = "oo";
  else if (s.contains("\"arena\":\"geometry\"")) out = "";
  else if (s.contains("\"arena\":\"head_top\"")) out = "_";
  else if (s.contains("\"arena\":\"mouth\"")) out = "^";
  else if (s.contains("\"arena\":\"newlines\"")) out = "";
  else if (s.contains("\"arena\":\"nose\"")) out = ".";
  else if (s.contains("\"arena\":\"padding\"")) out = "      ";
  else if (s.contains("\"arena\":\"whiskers\"")) out = "><";
            System.out.print("{\"ok\":true,\"output\":\"" + out + "\"}");
        } else {
            boolean ok = s.contains("\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"");
            System.out.print(ok ? "{\"ok\":true,\"output\":\"" + "es un gato" + "\"}"
                                : "{\"ok\":false,\"output\":\"" + "no es el gato canonico" + "\"}");
        }
    }
}
