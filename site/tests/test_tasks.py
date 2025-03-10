# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# CDS-RDM is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Task tests."""
from datetime import datetime, timedelta

from invenio_access.permissions import system_identity
from invenio_records_resources.proxies import current_service_registry
from invenio_search.engine import dsl
from invenio_vocabularies.contrib.names.api import Name

from cds_rdm.tasks import merge_duplicate_names_vocabulary, sync_local_accounts_to_names


def test_sync_and_merge_local_accounts_to_names(
    app, database, user_1, user_2, name_full_data
):
    """Test sync local accounts to names."""
    since = (datetime.now() - timedelta(days=1)).isoformat()
    # Sync user 1 and user 2 to names
    sync_local_accounts_to_names(since)

    Name.index.refresh()

    service = current_service_registry.get("names")
    names = service.scan(system_identity)
    assert len(list(names.hits)) == 2

    name_1 = service.read(system_identity, user_1.user_profile["person_id"])
    name_2 = service.read(system_identity, user_2.user_profile["person_id"])

    assert name_1.data["given_name"] == user_1.user_profile["given_name"]
    assert name_1.data["family_name"] == user_1.user_profile["family_name"]
    assert name_2.data["given_name"] == user_2.user_profile["given_name"]
    assert name_2.data["family_name"] == user_2.user_profile["family_name"]

    # Creates a new name with same orcid as user_1
    item = service.create(system_identity, name_full_data)
    id_ = item.id
    Name.index.refresh()

    # Merge duplicate names based on ORCID
    merge_duplicate_names_vocabulary()

    Name.index.refresh()
    read_item = service.read(system_identity, id_)
    assert read_item.data["given_name"] == name_full_data["given_name"]
    assert read_item.data["family_name"] == name_full_data["family_name"]
    assert read_item.data["props"]["department"] == user_1.user_profile["department"]

    deprecated_name = service.read(system_identity, user_1.user_profile["person_id"])
    assert deprecated_name.data["tags"] == ["unlisted"]

    updated_name = service.read(system_identity, name_full_data["id"])
    assert updated_name.data["props"]["department"] == user_1.user_profile["department"]
    assert len(updated_name.data["affiliations"]) == 2
    assert {"name": "CERN"} in updated_name.data["affiliations"]


def test_sync_name_with_existing_orcid(app, database, user_3, name_user_3):
    """Test sync name with existing ORCID."""
    service = current_service_registry.get("names")

    # Creates a new name with same orcid as user_3
    item = service.create(system_identity, name_user_3)
    id_ = item.id
    Name.index.refresh()
    since = (datetime.now() - timedelta(days=1)).isoformat()
    # Sync user 3 to names
    sync_local_accounts_to_names(since)

    Name.index.refresh()

    names = service.scan(system_identity)
    # There should be user 1, user 1 orcid value, user 2, user 3 and user 3 orcid value
    assert len(list(names.hits)) == 5

    filter = dsl.Q(
        "bool",
        must=[
            dsl.Q("term", **{"props.user_id": str(user_3.get_id())}),
        ],
    )

    # The ORCID value is present but the CDS name is created anyway unlisted
    os_name = service.search(system_identity, extra_filter=filter)
    assert os_name.total == 2

    cds_name = service.read(system_identity, user_3.user_profile["person_id"])
    assert cds_name.data["tags"] == ["unlisted"]

    name = service.read(system_identity, id_)

    # Orcid value got updated
    assert name.data["given_name"] == user_3.user_profile["given_name"]
    assert name.data["family_name"] == user_3.user_profile["family_name"]
    assert name.data["props"]["department"] == user_3.user_profile["department"]
    assert name.data["props"]["user_id"] == user_3.get_id()
    assert len(name.data["affiliations"]) == 1
    assert {"name": "CERN"} in name.data["affiliations"]
    # ORCID identifier
    assert len(name.data["identifiers"]) == 1
