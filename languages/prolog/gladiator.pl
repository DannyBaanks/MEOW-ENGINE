piece_table("\"arena\":\"cheeks\"", "()").
piece_table("\"arena\":\"ears\"", "/\\\\/\\\\").
piece_table("\"arena\":\"eyes\"", "oo").
piece_table("\"arena\":\"geometry\"", "").
piece_table("\"arena\":\"head_top\"", "_").
piece_table("\"arena\":\"mouth\"", "^").
piece_table("\"arena\":\"newlines\"", "").
piece_table("\"arena\":\"nose\"", ".").
piece_table("\"arena\":\"padding\"", "      ").
piece_table("\"arena\":\"whiskers\"", "><").
piece_of(S, Out) :-
  findall(V, ( piece_table(K, V), sub_string(S, _, _, _, K) ), Vs),
  ( Vs = [V|_] -> Out = V ; Out = "" ).
main :-
  read_line_to_string(user_input, S),
  (   sub_string(S, _, _, _, "\"discipline\":\"construct\"")
  ->  piece_of(S, Out),
      format("{\"ok\":true,\"output\":\"~w\"}", [Out])
  ;   (   sub_string(S, _, _, _, "\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"")
      ->  format("{\"ok\":true,\"output\":\"~s\"}", ["es un gato"])
      ;   format("{\"ok\":false,\"output\":\"~s\"}", ["no es el gato canonico"])
      )
  ).
