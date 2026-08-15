// languages/rust/src/main.rs
//! Gladiador Rust. Sin serde: solo hay que leer dos strings del request.
use std::io::Read;

fn field<'a>(src: &'a str, key: &str) -> Option<&'a str> {
    let pat = format!("\"{}\":\"", key);
    let start = src.find(&pat)? + pat.len();
    let rest = &src[start..];
    let mut end = 0usize;
    let bytes = rest.as_bytes();
    while end < bytes.len() {
        if bytes[end] == b'"' && (end == 0 || bytes[end - 1] != b'\\') {
            break;
        }
        end += 1;
    }
    Some(&rest[..end])
}

fn unescape(s: &str) -> String {
    let mut out = String::new();
    let mut it = s.chars();
    while let Some(c) = it.next() {
        if c != '\\' { out.push(c); continue; }
        match it.next() {
            Some('n') => out.push('\n'),
            Some('\\') => out.push('\\'),
            Some('"') => out.push('"'),
            Some(other) => out.push(other),
            None => {}
        }
    }
    out
}

fn escape(s: &str) -> String {
    s.replace('\\', "\\\\").replace('"', "\\\"").replace('\n', "\\n")
}

fn construct(arena: &str) -> &'static str {
    match arena {
        "ears" => "/\\/\\",
        "head_top" => "_",
        "cheeks" => "()",
        "eyes" => "oo",
        "nose" => ".",
        "whiskers" => "><",
        "mouth" => "^",
        "padding" => "      ",
        _ => "",
    }
}

fn validate(cat: &str) -> (bool, &'static str) {
    let rows: Vec<&str> = cat.split('\n').collect();
    if rows.len() != 3 { return (false, "filas != 3"); }
    let widths: Vec<usize> = rows.iter().map(|r| r.chars().count()).collect();
    if widths != vec![6, 7, 6] { return (false, "anchos != [6,7,6]"); }
    if cat.contains('\u{0}') { return (false, "hay un agujero en el gato"); }
    if rows[1].matches('o').count() != 2 { return (false, "el gato no tiene dos ojos"); }
    if rows[0].matches('/').count() != 2 { return (false, "el gato no tiene dos orejas"); }
    (true, "es un gato")
}

fn main() {
    let mut input = String::new();
    std::io::stdin().read_to_string(&mut input).ok();

    let cap = field(&input, "discipline").unwrap_or("");
    let arena = field(&input, "arena").unwrap_or("");

    if cap == "construct" {
        println!("{{\"ok\":true,\"output\":\"{}\"}}", escape(construct(arena)));
    } else if cap == "validate" {
        let cand = unescape(field(&input, "candidate").unwrap_or(""));
        let (ok, reason) = validate(&cand);
        println!("{{\"ok\":{},\"output\":\"{}\"}}", ok, escape(reason));
    } else {
        println!("{{\"ok\":false,\"output\":\"disciplina desconocida\"}}");
    }
}