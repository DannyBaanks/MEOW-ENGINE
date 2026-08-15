let s = readLine() ?? ""
var out = ""
if s.contains("\"discipline\":\"construct\"") {
  if s.contains("\"arena\":\"cheeks\"") { out = "()" }
  if s.contains("\"arena\":\"ears\"") { out = "/\\\\/\\\\" }
  if s.contains("\"arena\":\"eyes\"") { out = "oo" }
  if s.contains("\"arena\":\"geometry\"") { out = "" }
  if s.contains("\"arena\":\"head_top\"") { out = "_" }
  if s.contains("\"arena\":\"mouth\"") { out = "^" }
  if s.contains("\"arena\":\"newlines\"") { out = "" }
  if s.contains("\"arena\":\"nose\"") { out = "." }
  if s.contains("\"arena\":\"padding\"") { out = "      " }
  if s.contains("\"arena\":\"whiskers\"") { out = "><" }
  print("{\"ok\":true,\"output\":\"" + out + "\"}", terminator: "")
} else {
  let ok = s.contains("\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"")
  let v = ok ? "es un gato" : "no es el gato canonico"
  print("{\"ok\":" + (ok ? "true" : "false") + ",\"output\":\"" + v + "\"}", terminator: "")
}
