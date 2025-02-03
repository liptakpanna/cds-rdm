# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# CDS-RDM is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Transformer module."""

from invenio_vocabularies.datastreams.transformers import BaseTransformer


class InspireJsonTransformer(BaseTransformer):
    """INSPIRE JSON transformer."""

    def __init__(self, root_element=None, *args, **kwargs):
        """Initializes the transformer."""
        self.root_element = root_element
        super().__init__(*args, **kwargs)

    def apply(self, stream_entry, **kwargs):
        """TODO."""
