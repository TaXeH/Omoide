from dataclasses import dataclass


@dataclass
class Relocation:
    uuid: str
    realm_uuid: str
    theme_uuid: str
    group_uuid: str
    source_path: str
    width: int
    height: int
    operation_type: str
