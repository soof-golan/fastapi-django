import uuid


def uuid_generate_v1mc() -> uuid.UUID:
    """Return a version 1 UUID with a random node MAC address.

    Timestamp locality + randomness provide useful properties for indexing.

    Further reading on why this is a somewhat good idea:
     - https://www.postgresql.org/docs/current/uuid-ossp.html
     - https://www.edgedb.com/docs/stdlib/uuid#function::std::uuid_generate_v1mc
    - https://datatracker.ietf.org/doc/html/draft-peabody-dispatch-new-uuid-format-04

    Further reading on why uuid V4 is probably not the best idea:
    - https://www.edgedb.com/docs/stdlib/uuid#function::std::uuid_generate_v4
    """
    from uuid import _random_getnode  # type: ignore[attr-defined]

    return uuid.uuid1(node=_random_getnode())
