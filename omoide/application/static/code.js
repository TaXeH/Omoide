function alterPlus(x) {
    // rewrite + symbol in query into %2B
    let element = document.getElementById("query_element");
    element.value = element.value.replace('\+', '%2B')
}
