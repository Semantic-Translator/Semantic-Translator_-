# Archive workflow

Every development stage is delivered as a complete ZIP archive.

## Naming

```text
Semantic-Translator_vMAJOR.MINOR.PATCH.zip
```

## Rules

1. Each archive contains the full project.
2. Every archive has an updated `CHANGELOG.md`.
3. The version in `pyproject.toml` must match the archive name.
4. Large models and secrets are never included.
5. After upload to GitHub, create a commit and optionally a release tag.
