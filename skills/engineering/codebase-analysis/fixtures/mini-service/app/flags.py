FLAGS = {
    "strict-validation": True,
}


def is_enabled(name: str) -> bool:
    return bool(FLAGS.get(name, False))
