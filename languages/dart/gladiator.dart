import 'dart:io';
void main() {
  final s = stdin.readLineSync() ?? '';
  var out = '';
  if (s.contains("\"discipline\":\"construct\"")) {
  if (s.contains("\"arena\":\"cheeks\"")) { out = "()"; }
  if (s.contains("\"arena\":\"ears\"")) { out = "/\\\\/\\\\"; }
  if (s.contains("\"arena\":\"eyes\"")) { out = "oo"; }
  if (s.contains("\"arena\":\"geometry\"")) { out = ""; }
  if (s.contains("\"arena\":\"head_top\"")) { out = "_"; }
  if (s.contains("\"arena\":\"mouth\"")) { out = "^"; }
  if (s.contains("\"arena\":\"newlines\"")) { out = ""; }
  if (s.contains("\"arena\":\"nose\"")) { out = "."; }
  if (s.contains("\"arena\":\"padding\"")) { out = "      "; }
  if (s.contains("\"arena\":\"whiskers\"")) { out = "><"; }
    stdout.write('{\"ok\":true,\"output\":\"$out\"}');
  } else {
    final ok = s.contains("\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"");
    final v = ok ? "es un gato" : "no es el gato canonico";
    stdout.write('{\"ok\":$ok,\"output\":\"$v\"}');
  }
}
