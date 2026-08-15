s = STDIN.read
out = ""
if s.include?("\"discipline\":\"construct\"")
  out = "()" if s.include?("\"arena\":\"cheeks\"")
  out = "/\\\\/\\\\" if s.include?("\"arena\":\"ears\"")
  out = "oo" if s.include?("\"arena\":\"eyes\"")
  out = "" if s.include?("\"arena\":\"geometry\"")
  out = "_" if s.include?("\"arena\":\"head_top\"")
  out = "^" if s.include?("\"arena\":\"mouth\"")
  out = "" if s.include?("\"arena\":\"newlines\"")
  out = "." if s.include?("\"arena\":\"nose\"")
  out = "      " if s.include?("\"arena\":\"padding\"")
  out = "><" if s.include?("\"arena\":\"whiskers\"")
  print '{"ok":true,"output":"' + out + '"}'
else
  ok = s.include?("\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"")
  print '{"ok":' + (ok ? 'true' : 'false') + ',"output":"' + (ok ? "es un gato" : "no es el gato canonico") + '"}'
end
