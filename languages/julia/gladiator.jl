s = read(stdin, String)
out = ""
if occursin("\"discipline\":\"construct\"", s)
  if occursin("\"arena\":\"cheeks\"", s) out = "()" end
  if occursin("\"arena\":\"ears\"", s) out = "/\\\\/\\\\" end
  if occursin("\"arena\":\"eyes\"", s) out = "oo" end
  if occursin("\"arena\":\"geometry\"", s) out = "" end
  if occursin("\"arena\":\"head_top\"", s) out = "_" end
  if occursin("\"arena\":\"mouth\"", s) out = "^" end
  if occursin("\"arena\":\"newlines\"", s) out = "" end
  if occursin("\"arena\":\"nose\"", s) out = "." end
  if occursin("\"arena\":\"padding\"", s) out = "      " end
  if occursin("\"arena\":\"whiskers\"", s) out = "><" end
  print("{\"ok\":true,\"output\":\"$out\"}")
else
  local ok = occursin("\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"", s)
  local v = ok ? "es un gato" : "no es el gato canonico"
  print("{\"ok\":", ok, ",\"output\":\"$v\"}")
end
