function alterPlus(x) {
    // rewrite + symbol in query into %2B
    let element = document.getElementById("query_element");
    element.value = element.value.replaceAll("\+", "%2B")
    element.value = element.value.replaceAll(/\s+/g, " ")
}
