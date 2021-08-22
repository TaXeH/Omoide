function alterPlus() {
    // rewrite + symbol in query into %2B
    let element = document.getElementById("query_element");
    element.value = element.value.replaceAll("\+", "%2B")
    element.value = element.value.replaceAll(/\s+/g, " ")
}

function toggleTheme(theme_uuid) {
    // include or exclude theme from search
    let button = document.getElementById('toggle_' + theme_uuid)
    let element = document.getElementById('theme_' + theme_uuid)

    if (!button || !element) {
        alert('Failed to get theme element')
        return
    }

    let is_visible = visibility[theme_uuid]

    element.classList.toggle('nav-chosen-theme');

    if (is_visible) {
        button.text = 'Include'
        visibility[theme_uuid] = false
    } else {
        button.text = 'Exclude'
        visibility[theme_uuid] = true
    }
}

function switchThemeFolding(theme_uuid) {
    // show or hide list of groups for this theme
    let button = document.getElementById('fold_' + theme_uuid)
    let element = document.getElementById('groups_' + theme_uuid)

    if (!button || !element) {
        // theme can have no groups
        return
    }

    if (button.text === 'Fold') {
        button.text = 'Unfold'
        element.style.display = 'none'
    } else {
        button.text = 'Fold'
        element.style.display = 'block'
    }
}

function applyFiltering() {
    // got to search page with new query
    let searchParams = new URLSearchParams(window.location.search);
    let keys = Object.keys(visibility).filter(k => visibility[k])
    searchParams.set("active_themes", keys.join(','));
    window.location.href = '/search?' + searchParams.toString();
}

function selectAllThemes() {
    Object.keys(visibility).forEach(v => visibility[v] = true)

    for (const theme_uuid of Object.keys(visibility)) {
        let button = document.getElementById('toggle_' + theme_uuid)
        let element = document.getElementById('theme_' + theme_uuid)

        if (!button || !element) {
            continue
        }
        element.classList.add('nav-chosen-theme');
        button.text = 'Exclude'
    }
}

function dropAllThemes() {
    Object.keys(visibility).forEach(v => visibility[v] = false)

    for (const theme_uuid of Object.keys(visibility)) {
        let button = document.getElementById('toggle_' + theme_uuid)
        let element = document.getElementById('theme_' + theme_uuid)

        if (!button || !element) {
            continue
        }

        element.classList.remove('nav-chosen-theme');
        button.text = 'Include'
    }
}
