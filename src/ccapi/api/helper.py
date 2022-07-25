# imports - standard imports
import re
import datetime as dt
import collections

from ccapi.model import (
    User,
    Model,
    BooleanModel, InternalComponent, ExternalComponent,
    Regulator,
    Condition, ConditionType, ConditionState, ConditionRelation,
    Document,
    ConstraintBasedModel
)
from bpyutils.util.datetime    import now
from bpyutils.util.string      import (
    sanitize_html,
    sanitize_text,
    lower
)
from bpyutils.util.array       import sequencify
from ccapi._compat          import iteritems, iterkeys

def cc_datetime_to_datetime(datetime_, default = None, raise_err = False):
    datetime_object = default
    formats_        = [
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ]

    if datetime_:
        for format_ in formats_:
            try:
                datetime_object = dt.datetime.strptime(
                    datetime_,
                    format_   
                )
            except ValueError:
                if raise_err:
                    raise

    return datetime_object

def _section_type_to_dict_key(section_type):
    splits  = re.findall("[A-Z][^A-Z]*", section_type)
    key     = "_".join([s.lower() for s in splits])

    return key

def _merge_metadata_to_model(model, meta):
    for attr, value in iteritems(meta):
        setattr(model, attr, value)
    return model

def _format_condition_kwargs(data):
    return dict(
        type     = ConditionType.IF  if data["type"] == "IF_WHEN" else ConditionType.UNLESS,
        state    = ConditionState.ON if data["state"] == "ON" else ConditionState.OFF,
        relation = ConditionRelation.COOPERATIVE if data.get("speciesRelation") == "AND" else ConditionRelation.INDEPENDENT
    )

def _model_version_response_to_boolean_model(response, meta = { },
    users = None, parent = None, client = None):
    metadata = { }

    for key, data in iteritems(response):
        if "/" in key:
            model_id, model_version_id = list(map(int, key.split("/")))
        else:
            model_id         = None
            model_version_id = int(key)

        model = BooleanModel(name = meta.get("name"),
            version = model_version_id, client = client)

        if meta:
            model.created       = cc_datetime_to_datetime(meta["creationDate"])
            model.description   = meta["description"]

        if "score" in data:
            metadata["score"] = data["score"]["score"]

        component_map = dict()
        for component_id, component_data in iteritems(data["speciesMap"]):
            component_class = ExternalComponent \
                if component_data["external"] else InternalComponent
            component = component_class(id = int(component_id),
                name = component_data["name"])
            component.created = cc_datetime_to_datetime(
                component_data.get("creationDate"), default = now()
            )
            component.updated = cc_datetime_to_datetime(
                component_data.get("updateDate"),   default = now()
            )

            # Knowledge Base
            # page_id_found = None
            # for page_id, page_data in iteritems(data["pageMap"]):
            #     if page_data["speciesId"] == component.id:
            #         page_id_found = int(page_id)

            # sections = dict()
            # if page_id_found:
            #     for section_id, section_data in iteritems(data["sectionMap"]):
            #         if section_data["pageId"] == page_id_found:
            #             section_type = section_data.get("type")
            #             if section_type:
            #                 for _, content_data in iteritems(data["contentMap"]):
            #                     if content_data["sectionId"] == int(section_id):
            #                         text = sanitize_html(content_data["text"])
            #                         text = sanitize_text(text)
            #                         key  = _section_type_to_dict_key(section_type)

            #                         if not key in sections:
            #                             sections[key] = [ ]

            #                         sections[key].append({
            #                             "position": content_data["position"],
            #                             "text":     text
            #                         })

            #     sections_formatted = dict()
            #     for key, section in sections.items():
            #         sections_formatted[key] = "\n".join([i["text"]
            #             for i in sorted(section, key = lambda s: s["position"])])
            #     sections = sections_formatted

            # component.information       = sections
            component_map[component.id] = component

            model.add_component(component)

        sub_condition_map   = dict()
        for sub_condition_id, sub_condition_data in iteritems(data["subConditionMap"]):
            components = [ ]
            for _, sub_condition_species_data in iteritems(data["subConditionSpeciesMap"]):
                if sub_condition_species_data["subConditionId"] == int(sub_condition_id):
                    species_id = sub_condition_species_data["speciesId"]
                    components.append(component_map[species_id])

            sub_condition   = Condition(id = int(sub_condition_id),
                components  = components,
                **_format_condition_kwargs(sub_condition_data)
            )

            sub_condition_map[sub_condition.id] = dict({
                "condition_id":     sub_condition_data["conditionId"],
                "sub_condition":    sub_condition
            })

        condition_map   = dict()
        for condition_id, condition_data in iteritems(data["conditionMap"]):
            components  = [ ]
            for _, condition_species_data in iteritems(data["conditionSpeciesMap"]):
                if condition_species_data["conditionId"] == int(condition_id):
                    species_id = condition_species_data["speciesId"]
                    components.append(component_map[species_id])

            condition_kwargs = _format_condition_kwargs(condition_data)

            condition   = Condition(id = int(condition_id),
                components     = components,
                sub_conditions = [data["sub_condition"]
                    for _, data in iteritems(sub_condition_map)
                        if data["condition_id"] == int(condition_id)
                ],
                **condition_kwargs,
                
            )

            condition_map[condition.id] = dict({
                "regulator_id": condition_data["regulatorId"],
                "condition":    condition
            })

        regulator_map           = dict()
        component_regulator_map = dict()
        for regulator_id, regulator_data in iteritems(data["regulatorMap"]):
            regulator = Regulator(id = int(regulator_id),
                species     = component_map[regulator_data["regulatorSpeciesId"]],
                type        = lower(regulator_data["regulationType"]),
                conditions  = [data["condition"]
                    for _, data in iteritems(condition_map)
                        if data["regulator_id"] == int(regulator_id)
                ]
            )

            component_regulator_map[regulator.id] = dict({
                "component": component_map[regulator_data["speciesId"]],
                "regulator": regulator
            })

        for i, component in enumerate(model.components):
            if isinstance(component, InternalComponent):
                for regulator_id, component_regulator_data in iteritems(component_regulator_map):
                    if component == component_regulator_data["component"]:
                        model.components[i].regulators.append(
                            component_regulator_data["regulator"]
                        )

        metadata["users"] = [ ]
        for _, share_data in iteritems(data["shareMap"]):
            user = users.get_by_id(share_data["userId"])
            metadata["users"].append(user)

        model._references = []

        if "modelReferenceMap" in data:
            for _, model_reference_map_data in iteritems(data["modelReferenceMap"]):
                referenceId     = model_reference_map_data["referenceId"]
                reference_data  = data["referenceMap"][str(referenceId)]
                
                model._references.append({
                    "pmid": reference_data["pmid"],
                     "doi": reference_data["doi"]
                })

        return model, metadata

def _model_content_to_model(content, users, client = None):
    metadata          = content["metadata"]

    if "model" in metadata:
        data              = metadata["model"]

        model             = Model(id = int(data["id"]), name = data["name"],
            domain = data["type"], client = client)

        # HACK: remove default version provided.
        model.versions.pop()

        model.description = data["description"]
        model.author      = data["author"]
        model.tags        = data["tags"] and data["tags"].split(", ")

        model.citations   = data["cited"]

        model.created     = cc_datetime_to_datetime(data.get("creationDate")) or now()

        model.updated     = dict(
            biologic  = cc_datetime_to_datetime(data.get("biologicUpdateDate")),
            knowledge = cc_datetime_to_datetime(data.get("knowledgeBaseUpdateDate"))
        )

        model.public      = data["published"]

        model.user        = users.get_by_id(data["userId"])

        model.hash        = data.get("hash")

        model._parent_id  = data["originId"]

        model.permissions = metadata["modelPermissions"]
        
        for version_id, version_data in iteritems(content["versions"]):
            meta            = data["modelVersionMap"][str(version_id)]
            version, meta   = _model_version_response_to_boolean_model(
                response    = version_data,
                meta        = meta,
                users       = users,
                parent      = model,
                client      = client,
            )
            model           = _merge_metadata_to_model(model, meta)

            model.add_version(version)

        current_version   = data["selectedVersion"]
        for version in model.versions:
            if version.version == current_version:
                model.default_version = version

        if metadata["uploadMap"]:
            for _, upload_data in iteritems(metadata["uploadMap"]):
                document = Document(name = upload_data["uploadName"], client = client)

                document.user       = users.get_by_id(upload_data["userId"])
                document.created    = cc_datetime_to_datetime(upload_data["uploadDate"])
                document._token     = upload_data["token"]

                model.documents.append(document)

        return model
    else:
        data              = metadata

        model             = Model(id = int(data["id"]), name = data["name"],
            domain = data["domainType"], default_type = data["modelType"], client = client)

        # HACK: remove default version provided.
        model.versions.pop()

        model.description = data.get("description")
        model.score       = None
        # model.author      = data["author"]
        model.tags        = data["tags"] and data["tags"].split(", ")

        # model.citations   = data["cited"]

        model.created     = cc_datetime_to_datetime(data.get("_createdAt")) or now()
        model.updated     = cc_datetime_to_datetime(data.get("_updatedAt")) or now()

        # model.updated     = dict(
        #     biologic  = cc_datetime_to_datetime(data.get("biologicUpdateDate")),
        #     knowledge = cc_datetime_to_datetime(data.get("knowledgeBaseUpdateDate"))
        # )

        model.public      = data["public"]

        model.user        = users.get_by_id(int(data["_createdBy"]))

        # model.hash        = data.get("hash")

        # model._parent_id  = data["originId"]

        # model.permissions = metadata["modelPermissions"]

        model.__versions = data

        for version in data["versions"]:
            metabolic = ConstraintBasedModel()

            metabolic.description = data.get("description") or version.get("description") or None

            model.add_version(metabolic)
        
        # for version_id, version_data in iteritems(content["versions"]):
            # model.add_version(data)
            # print(data)
            
            # meta            = data["modelVersionMap"][str(version_id)]
            # version, meta   = _model_version_response_to_metabolic_model(
            #     response    = version_data,
            #     meta        = meta,
            #     users       = users,
            #     parent      = model,
            #     client      = client,
            # )
            # model           = _merge_metadata_to_model(model, meta)

            # model.add_version(version)

        # current_version   = data["selectedVersion"]
        # for version in model.versions:
        #     if version.version == current_version:
        #         model.default_version = version

        return model

def _user_response_to_user(response, client = None):
    user = User(id = int(response["id"]), first_name = response["firstName"],
        last_name = response["lastName"], client = client)

    user.email       = response.get("email")
    user.institution = response.get("institution")

    return user

def _build_model_urls(client, id_, version, hash_ = None):
    urls = dict()

    ids  = sequencify(id_)
    
    for id_ in ids:
        base_url = client._build_url("_api/model/get", id_,
            prefix = False)
        url      = None

        versions = [ ]

        if isinstance(version, collections.Mapping):
            if id_ in version:
                versions = sequencify(version[id_])
        else:
            versions = sequencify(version)

        for v in versions:
            params  = dict(version = v)
            url     = client._build_url(base_url, params = params,
                prefix = False)
            
            if hash_:
                if isinstance(hash_, str):
                    hash_ = dict({ id_: hash_ })
                
                for hash_id, hash_hash in iteritems(hash_):
                    if hash_id == id_:
                        url = "%s&%s" % (url, hash_hash)
            
            key         = "%s/%s" % (id_, v)

            urls[key]   = url

    return urls