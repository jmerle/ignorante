from ignorante.templates import find_templates, sort_key


def generate_gitignore(names: list[str]) -> str:
    """Fetch and combine the given gitignore templates into a single file."""
    if not names:
        return ""

    sorted_names = sorted((name.strip().lower() for name in names), key=sort_key)

    templates = find_templates()
    name_by_lower_name = {name.lower(): name for name in templates}

    sections = []
    for lower_name in sorted_names:
        name = name_by_lower_name.get(lower_name)

        if name is None:
            raise ValueError(f"Unknown gitignore template: {lower_name!r}")

        sections.append(f"### {name} ###\n{templates[name].read_text().strip()}")

    command = f"uvx ignorante {' '.join(sorted_names)}"
    header = f"# Created with https://github.com/jmerle/ignorante\n# Update by running `{command}`"
    footer = f"# End of `{command}`"

    return "\n\n".join([header, *sections, footer]) + "\n"
