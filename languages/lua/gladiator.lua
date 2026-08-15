local s = io.read('*a')
local out = ""
if s:find("\"discipline\":\"construct\"", 1, true) then
  if s:find("\"arena\":\"cheeks\"", 1, true) then out = "()"
  elseif s:find("\"arena\":\"ears\"", 1, true) then out = "/\\\\/\\\\"
  elseif s:find("\"arena\":\"eyes\"", 1, true) then out = "oo"
  elseif s:find("\"arena\":\"geometry\"", 1, true) then out = ""
  elseif s:find("\"arena\":\"head_top\"", 1, true) then out = "_"
  elseif s:find("\"arena\":\"mouth\"", 1, true) then out = "^"
  elseif s:find("\"arena\":\"newlines\"", 1, true) then out = ""
  elseif s:find("\"arena\":\"nose\"", 1, true) then out = "."
  elseif s:find("\"arena\":\"padding\"", 1, true) then out = "      "
  elseif s:find("\"arena\":\"whiskers\"", 1, true) then out = "><"
  end
  io.write('{"ok":true,"output":"' .. out .. '"}')
else
  if s:find("\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"", 1, true) then
    io.write('{"ok":true,"output":"' .. "es un gato" .. '"}')
  else
    io.write('{"ok":false,"output":"' .. "no es el gato canonico" .. '"}')
  end
end
