const fs = require('fs');
const s = fs.readFileSync(0, 'utf8').toString();
let out = '';
if (s.indexOf("\"discipline\":\"construct\"") >= 0) {
  if (s.indexOf("\"arena\":\"cheeks\"") >= 0) out = "()";
  else if (s.indexOf("\"arena\":\"ears\"") >= 0) out = "/\\\\/\\\\";
  else if (s.indexOf("\"arena\":\"eyes\"") >= 0) out = "oo";
  else if (s.indexOf("\"arena\":\"geometry\"") >= 0) out = "";
  else if (s.indexOf("\"arena\":\"head_top\"") >= 0) out = "_";
  else if (s.indexOf("\"arena\":\"mouth\"") >= 0) out = "^";
  else if (s.indexOf("\"arena\":\"newlines\"") >= 0) out = "";
  else if (s.indexOf("\"arena\":\"nose\"") >= 0) out = ".";
  else if (s.indexOf("\"arena\":\"padding\"") >= 0) out = "      ";
  else if (s.indexOf("\"arena\":\"whiskers\"") >= 0) out = "><";
  process.stdout.write('{"ok":true,"output":"' + out + '"}');
} else {
  const ok = s.indexOf("\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"") >= 0;
  process.stdout.write('{"ok":' + (ok ? 'true' : 'false') + ',"output":"' + (ok ? "es un gato" : "no es el gato canonico") + '"}');
}
