# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details
# http://www.gnu.org/licenses/gpl-3.0.txt

"""TUI and CLI specs for torrent details sections"""

from ..logging import make_logger
log = make_logger(__name__)

from functools import partial


def _size_hr(t):
    if t['size-total'] == t['size-final']:
        return '%s' % t['size-total'].with_unit
    else:
        return '%s (%s wanted)' % (t['size-total'].with_unit, t['size-final'].with_unit)

def _size_mr(t):
    return '%d\t%d' % (t['size-total'], t['size-final'])


def _files_hr(t):
    return '%d (%d wanted)' % (t['count-files'], t['count-files-wanted'])

def _files_mr(t):
    return '%d\t%d' % (t['count-files'], t['count-files-wanted'])


def _pieces_hr(t):
    return '%d * %s' % (t['count-pieces'], t['size-piece'].with_unit)

def _pieces_mr(t):
    return '%d\t%d' % (t['count-pieces'], t['size-piece'])


def _private_hr(t):
    return ('yes (decentralized peer discovery is disabled for this torrent)'
            if t['private'] else
            'no (decentralized peer discovery allowed if enabled globally)')

def _private_mr(t):
    return 'yes' if t['private'] else 'no'


def _uploaded_hr(t):
    return '%s (%.2f %%)' % (t['size-uploaded'].with_unit, t['%uploaded'])

def _uploaded_mr(t):
    return '%d\t%f' % (t['size-uploaded'], t['%uploaded'] / 100)


def _downloaded_hr(t):
    info = ['%.2f %%' % t['%downloaded']]
    if t['%downloaded'] < 100:
        if t['timespan-eta']:
            info.append('%s / %s left' % (t['size-left'].with_unit, t['timespan-eta']))
        else:
            info.append('%s left' % t['size-left'].with_unit)
    return '%s (%s)' % (t['size-downloaded'].with_unit, ', '.join(info))

def _downloaded_mr(t):
    return '%d\t%f\t%d\t%d' % (t['size-downloaded'],
                               t['%downloaded'] / 100, t['size-left'],
                               t['timespan-eta'])


def _available_hr(t):
    return '%s (%.2f %%)' % (t['size-available'].with_unit, t['%available'])

def _available_mr(t):
    return '%d\t%f' % (t['size-available'], t['%available'])


def _isolated_hr(t):
    status = t['status']
    return ('yes (torrent can\'t discover new peers)'
            if status.ISOLATED in status else
            'no (torrent can discover new peers)')

def _isolated_mr(t):
    status = t['status']
    return 'yes' if status.ISOLATED in status else 'no'


def _date_hr(key, t):
    date = t[key]
    if abs(date.delta) < 5:
        return 'now'
    return '%s (%s)' % (date.full, date.delta.with_preposition)

def _date_mr(key, t):
    date = t[key]
    return '%d\t%d' % (date, date.delta)


class Item():
    def __init__(self, label, needed_keys, human_readable=None, machine_readable=None):
        self.label = label
        self.needed_keys = needed_keys
        if human_readable is None:
            self.human_readable = lambda torrent, key=needed_keys[0]: str(torrent[key])
        else:
            self.human_readable = human_readable
        if machine_readable is None:
            self.machine_readable = self.human_readable
        else:
            self.machine_readable = machine_readable


SECTIONS = (
    {'title': 'Torrent', 'width': 60, 'items': (
        Item('Name',       ('name',)),
        Item('ID',         ('id',)),
        Item('Hash',       ('hash',)),
        Item('Size',       ('size-total', 'size-final'), _size_hr, _size_mr),
        Item('Files',      ('count-files', 'count-files-wanted'), _files_hr, _files_mr),
        Item('Pieces',     ('count-pieces', 'size-piece'), _pieces_hr, _pieces_mr),
        Item('Private',    ('private',), _private_hr, _private_mr),
        Item('Comment',    ('comment',)),
        Item('Creator',    ('creator',)),
    )},

    {'title': 'Status', 'width': 51, 'items': (
        Item('Location',   ('path',),),
        Item('Available',  ('%available', 'size-available'), _available_hr, _available_mr),
        Item('Downloaded', ('size-downloaded', 'size-left', '%downloaded', 'timespan-eta'), _downloaded_hr, _downloaded_mr),
        Item('Uploaded',   ('size-uploaded', 'size-total', '%uploaded'), _uploaded_hr, _uploaded_mr),
        Item('Ratio',      ('ratio',)),
        Item('Isolated',   ('status',), _isolated_hr, _isolated_mr),
    )},

    {'title': 'Peers', 'width': 25, 'items': (
        Item('Seeding peers',     ('peers-seeding',)),
        Item('Connected peers',   ('peers-connected',)),
        Item('Uploading peers',   ('peers-uploading',)),
        Item('Downloading peers', ('peers-downloading',)),
    )},

    {'title': 'Dates', 'width': 39, 'items': (
        Item('Created',    ('time-created',),   partial(_date_hr, 'time-created'),   partial(_date_mr, 'time-created')),
        Item('Added',      ('time-added',),     partial(_date_hr, 'time-added'),     partial(_date_mr, 'time-added')),
        Item('Started',    ('time-started',),   partial(_date_hr, 'time-started'),   partial(_date_mr, 'time-started')),
        Item('Completed',  ('time-completed',), partial(_date_hr, 'time-completed'), partial(_date_mr, 'time-completed')),
        Item('Active',     ('time-activity',),  partial(_date_hr, 'time-activity'),  partial(_date_mr, 'time-activity')),
    )},
)
