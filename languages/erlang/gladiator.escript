#!/usr/bin/env escript
main(_) ->
  S = io:get_line(""),
  case string:str(S, "\"discipline\":\"construct\"") > 0 of
    true  ->
      Out = piece(S),
      io:format("{\"ok\":true,\"output\":\"~s\"}", [Out]);
    false ->
      OK = string:str(S, "\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"") > 0,
      V = if OK -> "es un gato"; true -> "no es el gato canonico" end,
      BO = if OK -> "true"; true -> "false" end,
      io:format("{\"ok\":~s,\"output\":\"~s\"}", [BO, V])
  end,
  init:stop().
piece(S) ->
  L = [
      {"\"arena\":\"cheeks\"", "()"},
      {"\"arena\":\"ears\"", "/\\\\/\\\\"},
      {"\"arena\":\"eyes\"", "oo"},
      {"\"arena\":\"geometry\"", ""},
      {"\"arena\":\"head_top\"", "_"},
      {"\"arena\":\"mouth\"", "^"},
      {"\"arena\":\"newlines\"", ""},
      {"\"arena\":\"nose\"", "."},
      {"\"arena\":\"padding\"", "      "},
      {"\"arena\":\"whiskers\"", "><"},
    {"", ""}
  ],
  case [V || {K, V} <- L, K =/= "", string:str(S, K) > 0] of
    [V | _] -> V;
    [] -> ""
  end.
