from typing import List

from omoide import core
from omoide.use_cases.makemigrations.class_all_objects import AllObjects
from omoide.use_cases.makemigrations.class_relocation import Relocation


def instantiate_relocations(content_path: str,
                            all_objects: AllObjects,
                            relocations: List[Relocation],
                            filesystem: core.Filesystem) -> List[dict]:
    """Instantiate relocation instructions."""
    all_realms = {x.uuid: x for x in all_objects.realms}
    all_themes = {x.uuid: x for x in all_objects.themes}
    all_groups = {x.uuid: x for x in all_objects.groups}

    all_relocations: List[dict] = []

    for relocation in relocations:
        uuid = relocation.uuid
        realm_uuid = relocation.realm_uuid
        theme_uuid = relocation.theme_uuid
        group_uuid = relocation.group_uuid
        from_ = relocation.source_path

        if group_uuid in all_objects.groups:
            group_path = all_groups[group_uuid].route
        else:
            group_path = 'other'

        to_ = filesystem.join(
            content_path,
            all_realms[realm_uuid].route,
            all_themes[theme_uuid].route,
            group_path,
            f'{uuid}.jpg'
        )

        all_relocations.append({
            'from': filesystem.absolute(from_),
            'to': filesystem.absolute(to_),
            'width': relocation.width,
            'height': relocation.height,
            'operation_type': relocation.operation_type,
        })

    return all_relocations
