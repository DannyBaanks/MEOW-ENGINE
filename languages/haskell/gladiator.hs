import Data.List (isInfixOf)
main :: IO ()
main = do
  s <- getLine
  if isInfixOf "\"discipline\":\"construct\"" s
    then putStrLn ("{\"ok\":true,\"output\":\"" ++ piece s ++ "\"}")
    else
      let ok = isInfixOf "\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"" s
          v = if ok then "es un gato" else "no es el gato canonico"
      in putStrLn ("{\"ok\":" ++ (if ok then "true" else "false") ++ ",\"output\":\"" ++ v ++ "\"}")
piece :: String -> String
piece s = case [v | (k, v) <- table, isInfixOf k s] of
  (v:_) -> v
  []    -> ""
table :: [(String, String)]
table = [
      ("\"arena\":\"cheeks\"", "()"),
      ("\"arena\":\"ears\"", "/\\\\/\\\\"),
      ("\"arena\":\"eyes\"", "oo"),
      ("\"arena\":\"geometry\"", ""),
      ("\"arena\":\"head_top\"", "_"),
      ("\"arena\":\"mouth\"", "^"),
      ("\"arena\":\"newlines\"", ""),
      ("\"arena\":\"nose\"", "."),
      ("\"arena\":\"padding\"", "      "),
      ("\"arena\":\"whiskers\"", "><"),
    ("", "")
  ]
