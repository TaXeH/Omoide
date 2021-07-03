# # -*- coding: utf-8 -*-
#
# """Supporting code needed for SQL commands.
# """
# from typing import List
#
# from omoide import core
# from omoide.database import models
# from omoide.use_cases.make_migrations.class_all_objects import AllObjects
# from omoide.use_cases.make_migrations.class_sql import SQL
#
#
# def make_commands_for_realms(realms: List[core.Realm]) -> List[SQL]:
#     """Instantiate migration commands for realms."""
#     sql = []
#     for realm in realms:
#         stmt = models.realms.insert().values(uuid=realm.uuid,
#                                              route=realm.route,
#                                              label=realm.label)
#         sql.append(SQL(stmt))
#
#         for rule in realm.permissions:
#             sub_stmt = models.permissions_realms.insert().values(
#                 realm_uuid=realm.uuid,
#                 value=rule,
#             )
#             sql.append(SQL(sub_stmt))
#     return sql
#
#
# def make_commands_for_themes(themes: List[core.Theme]) -> List[SQL]:
#     """Instantiate migration commands for themes."""
#     sql = []
#     for theme in themes:
#         stmt = models.themes.insert().values(uuid=theme.uuid,
#                                              realm_uuid=theme.realm_uuid,
#                                              route=theme.route,
#                                              label=theme.label)
#         sql.append(SQL(stmt))
#
#         for rule in theme.permissions:
#             sub_stmt = models.permissions_themes.insert().values(
#                 realm_uuid=theme.uuid,
#                 value=rule,
#             )
#             sql.append(SQL(sub_stmt))
#
#         for tag in theme.implicit_tags:
#             sub_stmt = models.implicit_tags.insert().values(
#                 uuid=tag.uuid,
#                 theme_uuid=tag.theme_uuid,
#                 description=tag.description,
#             )
#             sql.append(SQL(sub_stmt))
#
#             for value in tag:
#                 sub_stmt = models.implicit_tags_values.insert().values(
#                     implicit_tag_uuid=tag.uuid,
#                     value=value,
#                 )
#                 sql.append(SQL(sub_stmt))
#
#         for synonym in theme.synonyms:
#             sub_stmt = models.synonyms.insert().values(
#                 uuid=synonym.uuid,
#                 theme_uuid=synonym.theme_uuid,
#                 description=synonym.description,
#             )
#             sql.append(SQL(sub_stmt))
#
#             for value in synonym:
#                 sub_stmt = models.synonyms_values.insert().values(
#                     synonym_uuid=synonym.uuid,
#                     value=value,
#                 )
#                 sql.append(SQL(sub_stmt))
#     return sql
#
#
# def make_commands_for_groups(groups: List[core.Group]) -> List[SQL]:
#     """Instantiate migration commands for groups."""
#     sql = []
#
#     for group in groups:
#         stmt = models.groups.insert().values(
#             uuid=group.uuid,
#             realm_uuid=group.realm_uuid,
#             theme_uuid=group.theme_uuid,
#             route=group.route,
#             label=group.label,
#             registered_on=group.registered_on,
#             registered_by=group.registered_by,
#             author=group.author,
#             author_url=group.author_url,
#             origin_url=group.origin_url,
#             comment=group.comment,
#             hierarchy=group.hierarchy,
#         )
#         sql.append(SQL(stmt))
#
#         for rule in group.permissions:
#             sub_stmt = models.permissions_groups.insert().values(
#                 realm_uuid=group.uuid,
#                 value=rule,
#             )
#             sql.append(SQL(sub_stmt))
#
#         for member in group.members:
#             sub_stmt = models.metas_to_groups.insert().values(
#                 group_uuid=group.uuid,
#                 meta_uuid=member,
#             )
#             sql.append(SQL(sub_stmt))
#
#     return sql
#
#
# def make_commands_for_implicit_tags(
#         implicit_tags: List[core.ImplicitTag]) -> List[SQL]:
#     """Instantiate migration commands for implicit tags."""
#     sql = []
#
#     for tag in implicit_tags:
#         stmt = models.implicit_tags.insert().values(
#             uuid=tag.uuid,
#             theme_uuid=tag.theme_uuid,
#             description=tag.description,
#         )
#         sql.append(SQL(stmt))
#
#         for value in tag:
#             sub_stmt = models.implicit_tags_values.insert().values(
#                 implicit_tag_uuid=tag.uuid,
#                 value=value,
#             )
#             sql.append(SQL(sub_stmt))
#     return sql
#
#
# def make_commands_for_synonyms(synonyms: List[core.Synonym]) -> List[SQL]:
#     """Instantiate migration commands for synonyms."""
#     sql = []
#
#     for synonym in synonyms:
#         stmt = models.synonyms.insert().values(
#             uuid=synonym.uuid,
#             theme_uuid=synonym.theme_uuid,
#             description=synonym.description,
#         )
#         sql.append(SQL(stmt))
#
#         for value in synonym:
#             sub_stmt = models.synonyms_values.insert().values(
#                 synonym_uuid=synonym.uuid,
#                 value=value,
#             )
#             sql.append(SQL(sub_stmt))
#
#     return sql
#
#
# def make_commands_for_metas(metas: List[core.Meta]) -> List[SQL]:
#     """Instantiate migration commands for metas."""
#     sql = []
#     for meta in metas:
#         stmt = models.metas.insert().values(
#             uuid=meta.uuid,
#             realm_uuid=meta.realm_uuid,
#             theme_uuid=meta.theme_uuid,
#             group_uuid=meta.group_uuid,
#             path_to_content=meta.path_to_content,
#             path_to_preview=meta.path_to_preview,
#             path_to_thumbnail=meta.path_to_thumbnail,
#             original_filename=meta.original_filename,
#             original_extension=meta.original_extension,
#             width=meta.width,
#             height=meta.height,
#             resolution=meta.resolution,
#             size=meta.size,
#             duration=meta.duration,
#             type=meta.type,
#             ordering=meta.ordering,
#             registered_on=meta.registered_on,
#             registered_by=meta.registered_by,
#             author=meta.author,
#             author_url=meta.author_url,
#             origin_url=meta.origin_url,
#             comment=meta.comment,
#             previous=meta.previous,
#             next=meta.next,
#             hierarchy=meta.hierarchy,
#             signature=meta.signature,
#             signature_type=meta.signature_type,
#         )
#         sql.append(SQL(stmt))
#
#         for rule in meta.permissions:
#             sub_stmt = models.permissions_metas.insert().values(
#                 meta_uuid=meta.uuid,
#                 value=rule,
#             )
#             sql.append(SQL(sub_stmt))
#
#     return sql
#
#
# def instantiate_commands(all_objects: AllObjects):
#     """Create all needed SQL instructions."""
#     sql: List[SQL] = []
#     sql.extend(make_commands_for_realms(all_objects.realms))
#     sql.extend(make_commands_for_themes(all_objects.themes))
#     sql.extend(make_commands_for_groups(all_objects.groups))
#     sql.extend(make_commands_for_implicit_tags(all_objects.implicit_tags))
#     sql.extend(make_commands_for_synonyms(all_objects.synonyms))
#     sql.extend(make_commands_for_metas(all_objects.metas))
#     return sql
