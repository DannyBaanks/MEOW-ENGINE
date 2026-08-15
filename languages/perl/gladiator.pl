my $s = <STDIN>;
my $out = "";
if (index($s, "\"discipline\":\"construct\"") >= 0) {
  if (index($s, "\"arena\":\"cheeks\"") >= 0) { $out = "()"; }
  if (index($s, "\"arena\":\"ears\"") >= 0) { $out = "/\\\\/\\\\"; }
  if (index($s, "\"arena\":\"eyes\"") >= 0) { $out = "oo"; }
  if (index($s, "\"arena\":\"geometry\"") >= 0) { $out = ""; }
  if (index($s, "\"arena\":\"head_top\"") >= 0) { $out = "_"; }
  if (index($s, "\"arena\":\"mouth\"") >= 0) { $out = "^"; }
  if (index($s, "\"arena\":\"newlines\"") >= 0) { $out = ""; }
  if (index($s, "\"arena\":\"nose\"") >= 0) { $out = "."; }
  if (index($s, "\"arena\":\"padding\"") >= 0) { $out = "      "; }
  if (index($s, "\"arena\":\"whiskers\"") >= 0) { $out = "><"; }
  print "{\"ok\":true,\"output\":\"$out\"}";
} else {
  my $ok = index($s, "\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"") >= 0;
  print $ok ? "{\"ok\":true,\"output\":\""."es un gato"."\"}"
            : "{\"ok\":false,\"output\":\""."no es el gato canonico"."\"}";
}
