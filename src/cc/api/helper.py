# imports - standard imports
import datetime as dt
import re
# import collections
# import random

# imports - third-party imports
import requests

# from cc.exception   import (
#     ValueError,
#     AuthenticationError,
#     HTTPError
# )
# from cc.config      import DEFAULT
# from cc.constant    import (
#     HEADER_AUTHENTICATION,
#     USER_AGENT,
#     MAXIMUM_API_RESOURCE_FETCH,
#     _AUTHENTICATION_ERROR_STRING
# )
from cc.model       import (
    Model,
    BooleanModel, InternalComponent, ExternalComponent,
    Regulator, Condition, SubCondition,
    Document
)
from cc.util.string import (
    sanitize_html,
    sanitize_text,
    lower
)
from cc.util.types  import (
    squash
)
# from cc.core.querylist import QueryList

# imports - third-party imports
from cc.model import User

def cc_datetime_to_python_datetime(datetime_, default = None,
    raise_err = False):
    datetime_object = default

    if datetime_:
        try:
            datetime_object = dt.datetime.strptime(
                datetime_,
                "%a, %d %b %Y %H:%M:%S %Z"
            )
        except ValueError:
            if raise_err:
                raise

    return datetime_object

def _user_response_object_to_user_object(client, response):
    user = User(id = int(response["id"]), first_name = response["firstName"],
        last_name = response["lastName"], client = client, autosave = False)

    user.email       = response.get("email")
    user.institution = response.get("institution")

    return user

def _section_type_to_dict_key(section_type):
    splits  = re.findall("[A-Z][^A-Z]*", section_type)
    key     = "_".join([s.lower() for s in splits])

    return key

def _model_version_response_object_to_model_object(client, response):
    _, data             = next(iter(response.items()))

    model               = BooleanModel(client = client)

    if "score" in data:
        model.score = data["score"]["score"]

    component_map = dict()
    for species_id, species_data in data["speciesMap"].items():
        component_class = InternalComponent \
            if species_data["external"] else ExternalComponent
        component = component_class(id = int(species_id), name = species_data["name"])
        component.created = cc_datetime_to_python_datetime(species_data["creationDate"])
        component.updated = cc_datetime_to_python_datetime(species_data["updateDate"])

        # knowledge base
        page_id_found = None
        for page_id, page_data in data["pageMap"].items():
            if page_data["speciesId"] == component.id:
                page_id_found = int(page_id)

        sections = dict()
        if page_id_found:
            for section_id, section_data in data["sectionMap"].items():
                if section_data["pageId"] == page_id_found:
                    section_type = section_data.get("type")
                    if section_type:
                        for _, content_data in data["contentMap"].items():
                            if content_data["sectionId"] == int(section_id):
                                text = sanitize_html(content_data["text"])
                                text = sanitize_text(text)
                                key  = _section_type_to_dict_key(section_type)

                                if not key in sections:
                                    sections[key] = [ ]

                                sections[key].append({
                                    "position": content_data["position"],
                                    "text":     text
                                })

            sections_formatted = dict()
            for key, section in sections.items():
                sections_formatted[key] = "\n".join([i["text"]
                    for i in sorted(section, key = lambda s: s["position"])])
            sections = sections_formatted

        component.information       = sections
        component_map[component.id] = component

        model.add_component(component)

    sub_condition_map   = dict()
    for sub_condition_id, sub_condition_data in data["subConditionMap"].items():
        species         = [ ]
        for _, sub_condition_species_data in data["subConditionSpeciesMap"].items():
            if sub_condition_species_data["subConditionId"] == int(sub_condition_id):
                species_id = sub_condition_species_data["speciesId"]
                species.append(component_map[species_id])

        sub_condition   = SubCondition(
            id          = int(sub_condition_id),
            type        = lower(sub_condition_data["type"]),
            operator    = lower(sub_condition_data["speciesRelation"])
                if sub_condition_data.get("speciesRelation") else None,
            state       = lower(sub_condition_data["state"]),
            species     = species
        )

        sub_condition_map[sub_condition.id] = dict({
            "condition_id":     sub_condition_data["conditionId"],
            "sub_condition":    sub_condition
        })

    condition_map   = dict()
    for condition_id, condition_data in data["conditionMap"].items():
        species     = [ ]
        for _, condition_species_data in data["conditionSpeciesMap"].items():
            if condition_species_data["conditionId"] == int(condition_id):
                species_id = condition_species_data["speciesId"]
                species.append(component_map[species_id])

        condition   = Condition(
            id                      = int(condition_id),
            sub_conditions          = [data["sub_condition"]
                for _, data in sub_condition_map.items()
                    if data["condition_id"] == int(condition_id)
            ],
            type                    = lower(condition_data["type"]),
            operator                = lower(condition_data["speciesRelation"])
                if condition_data.get("speciesRelation") else None,
            sub_condition_operator  = lower(condition_data["subConditionRelation"])
                if condition_data.get("subConditionRelation") else None,
            state                   = lower(condition_data["state"]),
            species                 = species
        )

        condition_map[condition.id] = dict({
            "regulator_id": condition_data["regulatorId"],
            "condition":    condition
        })

    regulator_map       = dict()
    for regulator_id, regulator_data in data["regulatorMap"].items():
        regulator           = Regulator(
            id              = int(regulator_id),
            type            = regulator_data["regulationType"].lower(),
            species         = component_map[regulator_data["regulatorSpeciesId"]],
            of              = component_map[regulator_data["speciesId"]],
            conditions      = [data["condition"]
                for _, data in condition_map.items()
                    if data["regulator_id"] == int(regulator_id)
            ]
        )

        regulator_map[regulator.id] = regulator

    for i, component in enumerate(model.components):
        if isinstance(component, InternalComponent):
            for regulator_id, regulator in regulator_map.items():
                if regulator.of == species:
                    model.components[i].regulators.append(regulator)

    model.permissions   = data.get("permissions")

    model.users         = [ ]
    for _, share_data in data["shareMap"].items():
        user = client.get("user", id = share_data["userId"])
        model.users.append(user)

    return model

def _model_response_object_to_model_object(client, response):
    data              = response["model"]

    model             = Model(id = int(data["id"]), name = data["name"],
        client = client)

    model.description = data["description"]
    model.author      = data["author"]
    model.tags        = data["tags"] and data["tags"].split(", ")

    model.domain      = data["type"]
    model.ncitations  = data["cited"]

    model.created     = cc_datetime_to_python_datetime(data["creationDate"])

    model.updated     = dict(
        biologic  = cc_datetime_to_python_datetime(data["biologicUpdateDate"]),
        knowledge = cc_datetime_to_python_datetime(data["knowledgeBaseUpdateDate"])
    )

    model.public      = data["published"]

    model.user        = client.get("user", id = data["userId"])

    model.hash        = data.get("hash")

    model.permissions = response["modelPermissions"]
    
    for version in data["modelVersionMap"].keys():
        model_version = client.get("model", id = model.id, version = version,
            hash = model.hash)

        model_version.id      = model.id
        model_version.version = version
        model_version.name    = model.name

        model.versions.append(model_version)

    if response["uploadMap"]:
        for _, upload_data in response["uploadMap"].items():
            document = Document(
                name        = upload_data["uploadName"],
                user        = client.get("user", id = upload_data["userId"]),
                created     = cc_datetime_to_python_datetime(
                    upload_data["uploadDate"]
                ),
                token       = upload_data["token"],
                client      = client
            )

            model.documents.append(document)

    return model