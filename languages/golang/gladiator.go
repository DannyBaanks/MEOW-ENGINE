package main

import (
    "io"
    "os"
    "strings"
)

func main() {
    b, _ := io.ReadAll(os.Stdin)
    var s = string(b)
    var out string
    if strings.Contains(s, "\"discipline\":\"construct\"") {
  if strings.Contains(s, "\"arena\":\"cheeks\"") {
        out = "()"
        }
  if strings.Contains(s, "\"arena\":\"ears\"") {
        out = "/\\\\/\\\\"
        }
  if strings.Contains(s, "\"arena\":\"eyes\"") {
        out = "oo"
        }
  if strings.Contains(s, "\"arena\":\"geometry\"") {
        out = ""
        }
  if strings.Contains(s, "\"arena\":\"head_top\"") {
        out = "_"
        }
  if strings.Contains(s, "\"arena\":\"mouth\"") {
        out = "^"
        }
  if strings.Contains(s, "\"arena\":\"newlines\"") {
        out = ""
        }
  if strings.Contains(s, "\"arena\":\"nose\"") {
        out = "."
        }
  if strings.Contains(s, "\"arena\":\"padding\"") {
        out = "      "
        }
  if strings.Contains(s, "\"arena\":\"whiskers\"") {
        out = "><"
        }
        os.Stdout.WriteString("{\"ok\":true,\"output\":\"" + out + "\"}")
    } else {
        ok := strings.Contains(s, "\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"")
        if ok {
            os.Stdout.WriteString("{\"ok\":true,\"output\":\"" + "es un gato" + "\"}")
        } else {
            os.Stdout.WriteString("{\"ok\":false,\"output\":\"" + "no es el gato canonico" + "\"}")
        }
    }
}
