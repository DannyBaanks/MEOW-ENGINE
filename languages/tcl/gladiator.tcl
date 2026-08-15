set s [gets stdin]
set out ""
if {[string first "\"discipline\":\"construct\"" $s] >= 0} {
  if {[string first "\"arena\":\"cheeks\"" $s] >= 0} { set out "()" }
  if {[string first "\"arena\":\"ears\"" $s] >= 0} { set out "/\\\\/\\\\" }
  if {[string first "\"arena\":\"eyes\"" $s] >= 0} { set out "oo" }
  if {[string first "\"arena\":\"geometry\"" $s] >= 0} { set out "" }
  if {[string first "\"arena\":\"head_top\"" $s] >= 0} { set out "_" }
  if {[string first "\"arena\":\"mouth\"" $s] >= 0} { set out "^" }
  if {[string first "\"arena\":\"newlines\"" $s] >= 0} { set out "" }
  if {[string first "\"arena\":\"nose\"" $s] >= 0} { set out "." }
  if {[string first "\"arena\":\"padding\"" $s] >= 0} { set out "      " }
  if {[string first "\"arena\":\"whiskers\"" $s] >= 0} { set out "><" }
  puts -nonewline "{\"ok\":true,\"output\":\"$out\"}"
} else {
  if {[string first "\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"" $s] >= 0} {
    set v "es un gato"
    set ok true
  } else {
    set v "no es el gato canonico"
    set ok false
  }
  puts -nonewline "{\"ok\":$ok,\"output\":\"$v\"}"
}
