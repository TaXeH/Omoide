# -*- coding: utf-8 -*-
from omoide.incarnation.freeze.freeze import act as act_freeze
from omoide.incarnation.make_migrations \
    .make_migrations import act as act_make_migrations
from omoide.incarnation.make_relocations \
    .make_relocations import act as act_make_relocations
from omoide.incarnation.migrate.migrate import act as act_migrate
from omoide.incarnation.relocate.relocate import act as act_relocate
from omoide.incarnation.runserver.runserver import act as act_runserver
from omoide.incarnation.show_tree.show_tree import act as act_show_tree
from omoide.incarnation.sync.sync import act as act_sync
from omoide.incarnation.unite.unite import act as act_unite
