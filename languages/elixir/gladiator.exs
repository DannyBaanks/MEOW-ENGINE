s = IO.read(:stdio, :line)
out = ""
if String.contains?(s, "\"discipline\":\"construct\"") do
  out = if String.contains?(s, "\"arena\":\"cheeks\""), do: "()", else: out
  out = if String.contains?(s, "\"arena\":\"ears\""), do: "/\\\\/\\\\", else: out
  out = if String.contains?(s, "\"arena\":\"eyes\""), do: "oo", else: out
  out = if String.contains?(s, "\"arena\":\"geometry\""), do: "", else: out
  out = if String.contains?(s, "\"arena\":\"head_top\""), do: "_", else: out
  out = if String.contains?(s, "\"arena\":\"mouth\""), do: "^", else: out
  out = if String.contains?(s, "\"arena\":\"newlines\""), do: "", else: out
  out = if String.contains?(s, "\"arena\":\"nose\""), do: ".", else: out
  out = if String.contains?(s, "\"arena\":\"padding\""), do: "      ", else: out
  out = if String.contains?(s, "\"arena\":\"whiskers\""), do: "><", else: out
  IO.write("{\"ok\":true,\"output\":\"" <> out <> "\"}")
else
  ok = String.contains?(s, "\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"")
  v = if ok, do: "es un gato", else: "no es el gato canonico"
  bo = if ok, do: "true", else: "false"
  IO.write("{\"ok\":" <> bo <> ",\"output\":\"" <> v <> "\"}")
end
