val s = readLine().orEmpty()
var output = ""
if (s.contains("\"discipline\":\"construct\"")) {
  if (s.contains("\"arena\":\"cheeks\"")) { output = "()" }
  if (s.contains("\"arena\":\"ears\"")) { output = "/\\\\/\\\\" }
  if (s.contains("\"arena\":\"eyes\"")) { output = "oo" }
  if (s.contains("\"arena\":\"geometry\"")) { output = "" }
  if (s.contains("\"arena\":\"head_top\"")) { output = "_" }
  if (s.contains("\"arena\":\"mouth\"")) { output = "^" }
  if (s.contains("\"arena\":\"newlines\"")) { output = "" }
  if (s.contains("\"arena\":\"nose\"")) { output = "." }
  if (s.contains("\"arena\":\"padding\"")) { output = "      " }
  if (s.contains("\"arena\":\"whiskers\"")) { output = "><" }
  print("{\"ok\":true,\"output\":\"$output\"}")
} else {
  if (s.contains("\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"")) print("{\"ok\":true,\"output\":\""+"es un gato"+"\"}")
  else print("{\"ok\":false,\"output\":\""+"no es el gato canonico"+"\"}")
}
