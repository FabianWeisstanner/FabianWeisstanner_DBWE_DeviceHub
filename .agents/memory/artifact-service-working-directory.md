---
name: Artifact service working directory
description: Relative paths in managed artifact service commands are resolved from the artifact directory.
---

Managed artifact service commands run with the artifact directory as their working directory rather than the workspace root. Root-level entrypoints therefore need a relative path such as `../../app.py` in the artifact command.

**Why:** The first Flask workflow failure showed that `python3 app.py` looked under `artifacts/devicehub`, while the entrypoint intentionally lives at the workspace root.

**How to apply:** When an artifact service launches a root-level script, use a path relative to `artifacts/<slug>` and verify it through the managed workflow before delivery.