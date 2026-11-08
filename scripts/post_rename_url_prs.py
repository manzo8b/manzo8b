#!/usr/bin/env python3
"""Prepare pull requests to migrate hard-coded URLs after a GitHub username change.

Default mode is read-only. --apply requires the new authenticated GitHub login.
Never rewrites ZIPs, binaries, local/browser data, historical git commits, or repo settings.
Requires GitHub CLI (gh), Git, and Python 3.10+.
"""
import argparse
import json
import subprocess
from pathlib import Path

EXTENSIONS = {
    ".md", ".html", ".htm", ".css", ".scss", ".js", ".mjs", ".cjs", ".ts",
    ".tsx", ".jsx", ".astro", ".json", ".xml", ".svg", ".yml", ".yaml",
    ".toml", ".txt", ".py", ".sh", ".webmanifest", ".rss",
}
SKIP_PARTS = {".git", "node_modules", "dist", "_site", "vendor", "coverage", ".next", ".astro"}
SKIP_NAMES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock"}
BRANCH = "chore/owner-url-migration-20261108"


def call(*args, cwd=None):
    done = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if done.returncode:
        raise RuntimeError(f"{' '.join(args)}: {done.stderr.strip() or done.stdout.strip()}")
    return done.stdout.strip()


def replacements(old, new):
    return [
        (f"https://{old}.github.io", f"https://{new}.github.io"),
        (f"http://{old}.github.io", f"https://{new}.github.io"),
        (f"https://raw.githubusercontent.com/{old}/", f"https://raw.githubusercontent.com/{new}/"),
        (f"https://api.github.com/repos/{old}/", f"https://api.github.com/repos/{new}/"),
        (f"git@github.com:{old}/", f"git@github.com:{new}/"),
        (f"https://github.com/{old}/", f"https://github.com/{new}/"),
        (f"http://github.com/{old}/", f"https://github.com/{new}/"),
        (f"https://github.com/{old}", f"https://github.com/{new}"),
    ]


def inspect_and_patch(folder, old, new, apply):
    files_changed, hits = [], 0
    tracked = call("git", "ls-files", "-z", cwd=folder).split("\0")
    for rel in tracked:
        if not rel:
            continue
        path = folder / rel
        if any(part in SKIP_PARTS for part in Path(rel).parts) or path.name in SKIP_NAMES:
            continue
        if path.suffix.lower() not in EXTENSIONS or not path.is_file() or path.is_symlink():
            continue
        if path.stat().st_size > 2_000_000:
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = original
        for before, after in replacements(old, new):
            hits += updated.count(before)
            updated = updated.replace(before, after)
        if updated != original:
            files_changed.append(rel)
            if apply:
                path.write_text(updated, encoding="utf-8")
    return files_changed, hits


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--old", default="manzo8b")
    ap.add_argument("--new", default="marcelo-fernandez")
    ap.add_argument("--apply", action="store_true", help="Create branches and PRs after the actual rename")
    ap.add_argument("--include-private", action="store_true", help="Include private repositories in this run")
    ap.add_argument("--workdir", default="github-username-migration")
    args = ap.parse_args()

    authenticated = call("gh", "api", "user", "--jq", ".login")
    if args.apply and authenticated.lower() != args.new.lower():
        raise SystemExit(f"BLOCKED: authenticated as {authenticated}; username must be {args.new} before --apply.")
    owner = args.new if args.apply else args.old
    raw = call("gh", "repo", "list", owner, "--limit", "200",
               "--json", "nameWithOwner,isPrivate,defaultBranchRef")
    repos = json.loads(raw)
    if not repos:
        raise SystemExit("No repositories found; check gh auth and username.")
    root = Path(args.workdir).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    print(f"Mode: {'create PRs' if args.apply else 'read-only inventory'}; owner: {owner}")
    for repo in repos:
        if repo["isPrivate"] and not args.include_private:
            print(f"SKIP private: {repo['nameWithOwner']} (use --include-private to include)")
            continue
        full_name = repo["nameWithOwner"]
        name = full_name.split("/", 1)[1]
        folder = root / name
        if folder.exists():
            print(f"SKIP existing clone: {folder} (use a new --workdir for a fresh run)")
            continue
        call("gh", "repo", "clone", full_name, str(folder), "--", "--quiet")
        changed, hits = inspect_and_patch(folder, args.old, args.new, args.apply)
        print(f"{full_name}: {len(changed)} text files / {hits} URL references")
        if not args.apply or not changed:
            continue
        base = repo.get("defaultBranchRef") or {}
        base_name = base.get("name", "main") if isinstance(base, dict) else "main"
        call("git", "checkout", "-b", BRANCH, cwd=folder)
        call("git", "add", "--", *changed, cwd=folder)
        call("git", "diff", "--cached", "--check", cwd=folder)
        call("git", "commit", "-m", "Update old GitHub owner and Pages URLs after username rename", cwd=folder)
        call("git", "push", "-u", "origin", BRANCH, cwd=folder)
        url = call("gh", "pr", "create", "--repo", full_name, "--base", base_name,
                   "--head", BRANCH, "--title", "Update owner and GitHub Pages URLs",
                   "--body", "Post-username migration: updates old GitHub and Pages URLs in tracked text files only. Review all generated/binary assets and verify deployment separately.")
        print(f"  REVIEW PR: {url}")
    print("Done. No PR is automatically merged; review build, Pages, SEO, and private integrations first.")


if __name__ == "__main__":
    main()
