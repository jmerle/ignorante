import questionary

from ignorante.templates import find_templates, sort_key


def select_templates() -> list[str]:
    """Prompt the user to interactively select gitignore templates.

    Returns the names of the selected templates, in their original casing.
    """
    names = sorted(find_templates(), key=sort_key)
    selected = questionary.checkbox(
        "Select gitignore templates to include",
        choices=names,
        use_jk_keys=False,
        use_search_filter=True,
    ).ask()

    if selected is None:
        raise RuntimeError("Aborted.")

    return selected
