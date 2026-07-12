# Semantic Knowledge Graph

## Structure

Each concept is represented by a Semantic-ID node.

```text
Semantic-ID
├── domain
├── multilingual labels
├── aliases
├── definition
├── metadata
└── vector
```

Relations are typed:

- `is-a`
- `part-of`
- `has-part`
- `related-to`
- `causes`
- `regulates`
- `located-in`
- `expressed-in`
- `derived-from`

## Search

Concept search combines:

- 60% vector similarity;
- 25% lexical similarity;
- 15% graph connectivity.

## Graph functions

- concept search;
- neighbors;
- shortest directed path;
- ontology validation;
- graph import and export.
