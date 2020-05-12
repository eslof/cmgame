import base64
import json
import secrets
from properties import Constants


def end(message="", code=0) -> None:
    if message:
        # TODO: does logging have a place here? does this method even make sense?
        print(message)
    quit(code)


def generate_id() -> str:
    return base64.b64encode(secrets.token_bytes(Constants.ID_TOKEN_BYTE_COUNT)).decode(
        "ascii"
    )


# TODO: Move some of these hard coded strings somewhere maybe


def sanitize_field(target, field, sanity, sanity_id="") -> None:
    if not hasattr(target, field) and field not in target:
        end(f"No sane index present ({sanity_id}): {json.dumps(target)}")
    elif not sanity(target[field]):
        end(f"Failed sanity check ({sanity_id}): {field} = {str(target[field])}")


def sanitize_json(target, field, sanity_id="") -> None:
    if not hasattr(target, field) and field not in target:
        end(f"No sane index present ({sanity_id}): {json.dumps(target)}")
    elif not isinstance(target[field], str) or not target[field]:
        end(f"Failed sanity check for json contents: {target[field]}")
    else:
        try:
            json.loads(target[field])
        except ValueError as e:
            end(f"Failed sanity check for json: {target[field]} {e}")
