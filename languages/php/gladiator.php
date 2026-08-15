<?php
$s = stream_get_contents(STDIN);
$out = "";
if (strpos($s, "\"discipline\":\"construct\"") !== false) {
  if (strpos($s, "\"arena\":\"cheeks\"") !== false) $out = "()";
  elseif (strpos($s, "\"arena\":\"ears\"") !== false) $out = "/\\\\/\\\\";
  elseif (strpos($s, "\"arena\":\"eyes\"") !== false) $out = "oo";
  elseif (strpos($s, "\"arena\":\"geometry\"") !== false) $out = "";
  elseif (strpos($s, "\"arena\":\"head_top\"") !== false) $out = "_";
  elseif (strpos($s, "\"arena\":\"mouth\"") !== false) $out = "^";
  elseif (strpos($s, "\"arena\":\"newlines\"") !== false) $out = "";
  elseif (strpos($s, "\"arena\":\"nose\"") !== false) $out = ".";
  elseif (strpos($s, "\"arena\":\"padding\"") !== false) $out = "      ";
  elseif (strpos($s, "\"arena\":\"whiskers\"") !== false) $out = "><";
  echo '{"ok":true,"output":"' . $out . '"}';
} else {
  $ok = strpos($s, "\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"") !== false;
  echo '{"ok":' . ($ok ? 'true' : 'false') . ',"output":"' . ($ok ? "es un gato" : "no es el gato canonico") . '"}';
}
