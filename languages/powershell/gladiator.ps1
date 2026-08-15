$s = [Console]::In.ReadToEnd()
$out = ""
if ($s.Contains('"discipline":"construct"')) {
  if ($s.Contains('"arena":"cheeks"')) { $out = '()' }
  if ($s.Contains('"arena":"ears"')) { $out = '/\\/\\' }
  if ($s.Contains('"arena":"eyes"')) { $out = 'oo' }
  if ($s.Contains('"arena":"geometry"')) { $out = '' }
  if ($s.Contains('"arena":"head_top"')) { $out = '_' }
  if ($s.Contains('"arena":"mouth"')) { $out = '^' }
  if ($s.Contains('"arena":"newlines"')) { $out = '' }
  if ($s.Contains('"arena":"nose"')) { $out = '.' }
  if ($s.Contains('"arena":"padding"')) { $out = '      ' }
  if ($s.Contains('"arena":"whiskers"')) { $out = '><' }
  Write-Output ('{"ok":true,"output":"' + $out + '"}')
} else {
  $ok = $s.Contains('"candidate":" /\\_/\\\n( o.o )\n > ^ <"')
  $v = if ($ok) { 'es un gato' } else { 'no es el gato canonico' }
  Write-Output ('{"ok":' + $ok.ToString().ToLower() + ',"output":"' + $v + '"}')
}
