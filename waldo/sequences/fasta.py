# -*- coding: utf-8 -*-
# Copyright (C) 2006-2010, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from collections import namedtuple

from waldo.tools import _gzip_open

sequence = namedtuple('sequence', 'header sequence')

def read(input):
    """
    for seq in read(input):
        ...

    Read a fasta file

    Iterates over the sequences in the file as `sequence` objects.
    comments (lines starting with ';') are ignored.

    Parameters
    ----------
      `input` : either a file or the name of a file.
    """
    if type(input) == str:
        if input.endswith('.gz'):
            input = _gzip_open(input)
        else:
            input = file(input)
    seq_items = []
    header = None
    for line in input:
        line = line.strip()
        if not line or line[0] == ';':
            continue
        elif line[0] == '>':
            if header is not None:
                seq = "".join(seq_items)
                seq_items = []
                yield sequence(header, seq)
            header = line[1:] # eat '>'
        else:
            seq_items.append(line)
    if header is not None:
        seq = "".join(seq_items)
        yield sequence(header, seq)

