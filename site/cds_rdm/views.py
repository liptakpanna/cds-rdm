# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2024 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CDS views."""


from flask import Blueprint, current_app, g, render_template
from flask_login import current_user
from invenio_communities import current_communities


def create_blueprint(app):
    """Blueprint for the routes and resources provided by Invenio-App-RDM."""
    blueprint = Blueprint(
        "cds_rdm_bp",
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    blueprint.add_url_rule("/", "index", view_func=index)
    return blueprint


def index():
    """Frontpage."""
    featured_communities_search = current_communities.service.featured_search(
        g.identity
    )

    featured = featured_communities_search.to_dict()["hits"]["hits"]
    if current_user.is_authenticated:
        my_comms = current_communities.service.search_user_communities(g.identity)
        my_comms = my_comms.to_dict()["hits"]["hits"]
    else:
        my_comms = None
    context = {"featured_communities": featured, "my_communities": my_comms}

    return render_template(
        current_app.config["THEME_FRONTPAGE_TEMPLATE"],
        show_intro_section=current_app.config["THEME_SHOW_FRONTPAGE_INTRO_SECTION"],
        **context,
    )
