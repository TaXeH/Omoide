function alterPlus() {
    // rewrite + symbol in query into %2B
    let element = document.getElementById("query_element");
    element.value = element.value.replaceAll("\+", "%2B")
    element.value = element.value.replaceAll(/\s+/g, " ")
}

function toggleTheme(theme_uuid) {
    // include or exclude theme from search
    let element = document.getElementById('theme_' + theme_uuid)

    if (!element) {
        alert('Failed to get theme element')
        return
    }

    let is_visible = visibility[theme_uuid]
    element.classList.toggle('nav-chosen-theme');
    visibility[theme_uuid] = !is_visible;
}

function switchThemeFolding(theme_uuid) {
    // show or hide list of groups for this theme
    let image = document.getElementById('fold_' + theme_uuid)
    let element = document.getElementById('groups_' + theme_uuid)

    if (!element) {
        // theme can have no groups
        return
    }

    if (element.style.display === 'none' || !element.style.display) {
        image.src = "../static/collapse-arrow.svg";
        element.style.display = 'block'
    } else {
        image.src = "../static/expand-arrow.svg";
        element.style.display = 'none'
    }
}

function applyFiltering() {
    // got to search page with new query
    let searchParams = new URLSearchParams(window.location.search);
    let keys = Object.keys(visibility).filter(k => visibility[k])
    searchParams.set("active_themes", keys.join(','));
    window.location.href = "/search?" + searchParams.toString();
}

function toggleAllThemes(checked) {
    // set all themes as active/inactive
    Object.keys(visibility).forEach(v => visibility[v] = !checked)

    for (const theme_uuid of Object.keys(visibility)) {
        let element = document.getElementById('toggle_' + theme_uuid)
        let checkmark = document.getElementById('checkmark_' + theme_uuid)

        if (!element || !checkmark) {
            continue
        }

        if (checked !== element.checked) {
            checkmark.click();
        }
    }
}

function explainSearchResults() {
    // toggle explanation block
    let element = document.getElementById('explain')

    if (!element)
        return

    if (element.style.display === 'none' || !element.style.display) {
        element.style.display = 'grid'
    } else {
        element.style.display = 'none'
    }
}
