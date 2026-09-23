module Box

helper value =
  value + 1

greet value =
  helper value * 2

runner =
  greet 3
