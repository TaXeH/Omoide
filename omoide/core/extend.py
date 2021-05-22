from omoide import core


def theme_from_realm(theme: core.Theme, realm: core.Realm) -> core.Theme:
    theme.permissions = theme.permissions.union(realm.permissions)
    return theme


def group_from_theme(group: core.Group, theme: core.Theme) -> core.Group:
    group.permissions = group.permissions.union(theme.permissions)
    return group


def meta_from_all(meta: core.Meta, realm: core.Realm,
                  theme: core.Theme, group: core.Group) -> core.Meta:
    print(meta)
    return meta
