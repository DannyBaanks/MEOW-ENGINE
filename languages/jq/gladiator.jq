
. as $s
| if ($s | contains("\"discipline\":\"construct\"")) then
    (             if ($s | contains("\"arena\":\"cheeks\"")) then {ok: true, output: "()"}
            elif ($s | contains("\"arena\":\"ears\"")) then {ok: true, output: "/\\/\\"}
            elif ($s | contains("\"arena\":\"eyes\"")) then {ok: true, output: "oo"}
            elif ($s | contains("\"arena\":\"geometry\"")) then {ok: true, output: ""}
            elif ($s | contains("\"arena\":\"head_top\"")) then {ok: true, output: "_"}
            elif ($s | contains("\"arena\":\"mouth\"")) then {ok: true, output: "^"}
            elif ($s | contains("\"arena\":\"newlines\"")) then {ok: true, output: ""}
            elif ($s | contains("\"arena\":\"nose\"")) then {ok: true, output: "."}
            elif ($s | contains("\"arena\":\"padding\"")) then {ok: true, output: "      "}
            elif ($s | contains("\"arena\":\"whiskers\"")) then {ok: true, output: "><"}
      else {ok: true, output: ""} end )
  elif ($s | contains("\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"")) then {ok: true, output: "es un gato"}
  else {ok: false, output: "no es el gato canonico"}
  end
