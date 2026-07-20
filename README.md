# Ignorante

A CLI for generating `.gitignore` files by combining templates from the [github/gitignore](https://github.com/github/gitignore) repository.

## Usage

### Direct mode

Pass one or more template names as arguments. Their `.gitignore` contents are concatenated and written to stdout:

```sh
uvx ignorante python node > .gitignore
```

Write to a file directly with `-o`/`--output` instead of piping stdout:

```sh
uvx ignorante python node --output .gitignore
```

Template names are matched case-insensitively against the filenames in the github/gitignore repository (e.g. `python` matches [`Python.gitignore`](https://github.com/github/gitignore/blob/main/Python.gitignore)).

Templates in the repository's `Global/` and `community/` subdirectories are referenced with a matching prefix:

```sh
uvx ignorante python global/linux community/golang/hugo
```

Here, `global/linux` matches [`Global/Linux.gitignore`](https://github.com/github/gitignore/blob/main/Global/Linux.gitignore) and `community/golang/hugo` matches [`community/Golang/Hugo.gitignore`](https://github.com/github/gitignore/blob/main/community/Golang/Hugo.gitignore).

### Interactive mode

Run with no arguments to pick templates interactively:

```sh
uvx ignorante
```

This opens a searchable, multi-select prompt listing every available template. Confirm your selection to write the combined `.gitignore` to stdout (or to a file, if `--output` is given).
