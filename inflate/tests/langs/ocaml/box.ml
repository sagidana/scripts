module Box = struct
  let helper value =
    value + 1

  let greet value =
    helper value * 2

  let runner () =
    greet 3
end
