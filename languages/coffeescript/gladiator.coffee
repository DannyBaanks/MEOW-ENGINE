fs = require 'fs'
s = fs.readFileSync(0, 'utf8').toString()
out = ''
if 0 <= s.indexOf("\"discipline\":\"construct\"")
  out = "()" if 0 <= s.indexOf("\"arena\":\"cheeks\"")
  out = "/\\\\/\\\\" if 0 <= s.indexOf("\"arena\":\"ears\"")
  out = "oo" if 0 <= s.indexOf("\"arena\":\"eyes\"")
  out = "" if 0 <= s.indexOf("\"arena\":\"geometry\"")
  out = "_" if 0 <= s.indexOf("\"arena\":\"head_top\"")
  out = "^" if 0 <= s.indexOf("\"arena\":\"mouth\"")
  out = "" if 0 <= s.indexOf("\"arena\":\"newlines\"")
  out = "." if 0 <= s.indexOf("\"arena\":\"nose\"")
  out = "      " if 0 <= s.indexOf("\"arena\":\"padding\"")
  out = "><" if 0 <= s.indexOf("\"arena\":\"whiskers\"")
  process.stdout.write '{"ok":true,"output":"' + out + '"}'
else
  ok = 0 <= s.indexOf("\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"")
  process.stdout.write '{"ok":' + (if ok then 'true' else 'false') + ',"output":"' + (if ok then "es un gato" else "no es el gato canonico") + '"}'
