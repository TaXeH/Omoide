from typing import Dict

from sqlalchemy import select
from sqlalchemy.engine import Engine

from omoide import core
from omoide.database import models


def get_all_realms(database: Engine) -> Dict[core.UUID, core.Realm]:
    """"""
    output = {}
    with database.begin() as conn:
        stmt = select(models.realms)
        rows = conn.execute(stmt).all()
        for row in rows:
            uuid, route, label = row
            realm = core.Realm(
                uuid=core.UUID(uuid),
                route=route,
                label=label,
            )
            output[realm.uuid] = realm
            sub_stmt = select(models.permissions_realms) \
                .where(models.permissions_realms.c.realm_uuid == realm.uuid)
            sub_rows = conn.execute(sub_stmt).all()
            permissions = set()
            for sub_row in sub_rows:
                _, permission = sub_row
                permissions.add(permission)
            realm.permissions = frozenset(permissions)

    return output


def get_all_themes(database: Engine) -> Dict[core.UUID, core.Theme]:
    """"""
    output = {}
    with database.begin() as conn:
        stmt = select(models.themes)
        rows = conn.execute(stmt).all()
        for row in rows:
            uuid, realm_uuid, route, label = row
            theme = core.Theme(
                uuid=core.UUID(uuid),
                realm_uuid=core.UUID(realm_uuid),
                route=route,
                label=label,
            )
            output[theme.uuid] = theme

            sub_stmt = select(models.permissions_themes) \
                .where(models.permissions_themes.c.theme_uuid == theme.uuid)
            sub_rows = conn.execute(sub_stmt).all()
            permissions = set()
            for sub_row in sub_rows:
                _, permission = sub_row
                permissions.add(permission)
            theme.permissions = frozenset(permissions)

            sub_stmt = select(models.synonyms) \
                .where(models.synonyms.c.theme_uuid == theme.uuid)
            sub_rows = conn.execute(sub_stmt).all()
            all_synonyms = []
            for sub_row in sub_rows:
                synonym_uuid, theme_uuid, descr = sub_row
                synonym = core.Synonym(
                    uuid=core.UUID(synonym_uuid),
                    theme_uuid=core.UUID(theme_uuid),
                    description=descr,
                )
                all_synonyms.append(synonym)

                sub_sub_stmt = select(models.synonyms_values) \
                    .where(
                    models.synonyms_values.c.synonym_uuid == synonym_uuid)
                sub_sub_rows = conn.execute(sub_sub_stmt).all()
                all_values = []
                for sub_sub_row in sub_sub_rows:
                    _, value = sub_sub_row
                    all_values.append(value)
                synonym.values = all_values
            theme.synonyms = all_synonyms

    return output


def get_all_groups(database: Engine) -> Dict[core.UUID, core.Group]:
    """"""
    output = {}
    with database.begin() as conn:
        stmt = select(models.groups)
        rows = conn.execute(stmt).all()
        for row in rows:
            (uuid, realm_uuid, theme_uuid, route,
             label, reg_on, reg_by, auth, aurl, ourl, comment, hi) = row
            group = core.Group(
                uuid=core.UUID(uuid),
                realm_uuid=core.UUID(realm_uuid),
                theme_uuid=core.UUID(theme_uuid),
                route=route,
                label=label,
                registered_on=reg_on,
                registered_by=reg_by,
                author=auth,
                author_url=aurl,
                origin_url=ourl,
                comment=comment,
                hierarchy=hi,
            )
            output[group.uuid] = group

            sub_stmt = select(models.permissions_groups) \
                .where(models.permissions_groups.c.group_uuid == group.uuid)
            sub_rows = conn.execute(sub_stmt).all()
            permissions = set()
            for sub_row in sub_rows:
                _, permission = sub_row
                permissions.add(permission)
            group.permissions = frozenset(permissions)

            sub_sub_stmt = select(models.metas_to_groups) \
                .where(models.metas_to_groups.c.group_uuid == group.uuid)
            sub_sub_rows = conn.execute(sub_sub_stmt).all()
            members = []
            for sub_sub_row in sub_sub_rows:
                group_uuid, meta_uuid = sub_sub_row
                members.append(meta_uuid)
            group.members = frozenset(members)

    return output


def get_all_metas(database: Engine) -> Dict[core.UUID, core.Meta]:
    """"""
    output = {}
    with database.begin() as conn:
        stmt = select(models.metas)
        rows = conn.execute(stmt).all()
        for row in rows:
            (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content,
             path_to_preview, path_to_thumbnail, original_filename,
             original_extension, width, height, resolution, size, duration,
             _type, ordering, registered_on, registered_by, author, author_url,
             origin_url, comment, signature, signature_type, previous, _next,
             hierarchy) = row
            meta = core.Meta(
                uuid=core.UUID(uuid),
                realm_uuid=core.UUID(realm_uuid),
                theme_uuid=core.UUID(theme_uuid),
                group_uuid=core.UUID(group_uuid),
                path_to_content=path_to_content,
                path_to_preview=path_to_preview,
                path_to_thumbnail=path_to_thumbnail,
                original_filename=original_filename,
                original_extension=original_extension,
                width=width,
                height=height,
                resolution=resolution,
                size=size,
                duration=duration,
                type=_type,
                ordering=ordering,
                registered_on=registered_on,
                registered_by=registered_by,
                author=author,
                author_url=author_url,
                origin_url=origin_url,
                comment=comment,
                signature=signature,
                signature_type=signature_type,
                previous=previous,
                next=_next,
                hierarchy=hierarchy,
            )
            output[meta.uuid] = meta

            sub_stmt = select(models.permissions_metas) \
                .where(models.permissions_metas.c.meta_uuid == meta.uuid)
            sub_rows = conn.execute(sub_stmt).all()
            permissions = set()
            for sub_row in sub_rows:
                _, permission = sub_row
                permissions.add(permission)
            meta.permissions = frozenset(permissions)

            sub_sub_stmt = select(models.meta_tags) \
                .where(models.meta_tags.c.meta_uuid == meta.uuid)
            sub_sub_rows = conn.execute(sub_sub_stmt).all()
            tags = []
            for sub_sub_row in sub_sub_rows:
                meta_uuid, meta_value = sub_sub_row
                tags.append(meta_value)
            meta.tags = frozenset(tags)

    return output


def get_all_users(database: Engine) -> Dict[core.UUID, core.User]:
    """"""
    return {}
