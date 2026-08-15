#lang racket
(define s (read-line (current-input-port) 'any))
(define out "")
(if (string-contains? s "\"discipline\":\"construct\"")
  (begin
  (when (string-contains? s "\"arena\":\"cheeks\"") (set! out "()"))
  (when (string-contains? s "\"arena\":\"ears\"") (set! out "/\\\\/\\\\"))
  (when (string-contains? s "\"arena\":\"eyes\"") (set! out "oo"))
  (when (string-contains? s "\"arena\":\"geometry\"") (set! out ""))
  (when (string-contains? s "\"arena\":\"head_top\"") (set! out "_"))
  (when (string-contains? s "\"arena\":\"mouth\"") (set! out "^"))
  (when (string-contains? s "\"arena\":\"newlines\"") (set! out ""))
  (when (string-contains? s "\"arena\":\"nose\"") (set! out "."))
  (when (string-contains? s "\"arena\":\"padding\"") (set! out "      "))
  (when (string-contains? s "\"arena\":\"whiskers\"") (set! out "><"))
    (printf "{\"ok\":true,\"output\":\"~a\"}" out))
  (let* ([ok (string-contains? s "\"candidate\":\" /\\\\_/\\\\\\n( o.o )\\n > ^ <\"")]
         [v (if ok "es un gato" "no es el gato canonico")]
         [bo (if ok "true" "false")])
    (printf "{\"ok\":~a,\"output\":\"~a\"}" bo v)))
