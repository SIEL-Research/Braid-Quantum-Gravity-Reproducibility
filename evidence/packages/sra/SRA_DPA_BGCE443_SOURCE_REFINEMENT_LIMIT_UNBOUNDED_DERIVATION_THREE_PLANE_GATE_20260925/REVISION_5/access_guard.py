#!/usr/bin/env python3
"""Path-contained allowlist/denylist guard for a later BGCE443 focal constructor."""

from __future__ import annotations

import fnmatch
import hashlib
from pathlib import Path


class AccessDenied(RuntimeError):
    pass


def guarded_read(repo_root: Path, relative_path: str, allowed: dict[str, str], deny_globs: list[str]) -> bytes:
    candidate = Path(relative_path)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise AccessDenied("NON_RELATIVE_OR_TRAVERSAL_PATH")
    normalized = candidate.as_posix()
    if any(fnmatch.fnmatch(normalized, pattern) for pattern in deny_globs):
        raise AccessDenied("DENYLIST_MATCH")
    if normalized not in allowed:
        raise AccessDenied("NOT_ALLOWLISTED")
    root = repo_root.resolve(strict=True)
    target = repo_root.joinpath(candidate)
    if target.is_symlink() or any(parent.is_symlink() for parent in [target, *target.parents] if parent != root.parent):
        raise AccessDenied("SYMLINK_PATH")
    resolved = target.resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise AccessDenied("OUTSIDE_REPOSITORY")
    payload = resolved.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != allowed[normalized]:
        raise AccessDenied("HASH_MISMATCH")
    return payload
