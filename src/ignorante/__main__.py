import sys
from pathlib import Path
from typing import Annotated

from typer import Argument, Exit, Option, Typer

from ignorante import __version__
from ignorante.generate import generate_gitignore
from ignorante.interactive import select_templates

app = Typer(context_settings={"help_option_names": ["--help", "-h"]}, add_completion=False)


def version_callback(value: bool) -> None:
    if value:
        print(__version__)
        raise Exit()


@app.command()
def cli(
    templates: Annotated[
        list[str] | None,
        Argument(help="Names of gitignore templates to combine. Omit to select templates interactively."),
    ] = None,
    output: Annotated[
        Path | None,
        Option("-o", "--output", help="Write the generated .gitignore to this file instead of stdout."),
    ] = None,
    version: Annotated[
        bool | None,
        Option("-v", "--version", help="Print the version and exit.", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    try:
        names = templates if templates else select_templates()
        content = generate_gitignore(names)
    except (RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        raise Exit(1) from error

    if output is not None:
        output.write_text(content)
    else:
        print(content, end="")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
