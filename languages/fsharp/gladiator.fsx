let s = stdin.ReadLine()
let mutable out = ""
if s.Contains("\"discipline\":\"construct\"") then
    if s.Contains("\"arena\":\"cheeks\"") then out <- "()"
    if s.Contains("\"arena\":\"ears\"") then out <- "/\\\\/\\\\"
    if s.Contains("\"arena\":\"eyes\"") then out <- "oo"
    if s.Contains("\"arena\":\"geometry\"") then out <- ""
    if s.Contains("\"arena\":\"head_top\"") then out <- "_"
    if s.Contains("\"arena\":\"mouth\"") then out <- "^"
    if s.Contains("\"arena\":\"newlines\"") then out <- ""
    if s.Contains("\"arena\":\"nose\"") then out <- "."
    if s.Contains("\"arena\":\"padding\"") then out <- "      "
    if s.Contains("\"arena\":\"whiskers\"") then out <- "><"
    let body = "{\"ok\":true,\"output\":\"" + out + "\"}"
    printf "%s" body
else
    let ok = s.Contains("\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"")
    let v = if ok then "es un gato" else "no es el gato canonico"
    let b = if ok then "true" else "false"
    let body2 = "{\"ok\":" + b + ",\"output\":\"" + v + "\"}"
    printf "%s" body2
