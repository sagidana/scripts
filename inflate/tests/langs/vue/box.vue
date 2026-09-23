<script>
function helper(value) {
    return value + 1;
}

function greet(value) {
    return helper(value) * 2;
}

function runner() {
    return greet(3);
}
</script>

<template><span>ok</span></template>
