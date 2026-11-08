# GitHub username migration — manzo8b → marcelo-fernandez

**Planning date:** 8 November 2026  
**Status:** prepared, **NOT executed**. Do not change public site links ahead of the account rename.

## Objective

Present the public developer identity as **Marcelo Fernandez** under the preferred GitHub username `marcelo-fernandez`, while preserving existing projects, issues, stars, source history, and site availability. The chosen username must be confirmed as available in GitHub Settings; absence from a public search does not reserve it.

## Inventory (verified through the connected GitHub account)

**15 repositories: 9 public, 6 private.** No visibility changes are authorized.

Public:
- `manzo8b` — special GitHub profile README, must eventually become `marcelo-fernandez`.
- `marcelus` — portfolio: `https://manzo8b.github.io/marcelus/`.
- `manzo-ai` — education: `https://manzo8b.github.io/manzo-ai/`.
- `risto-lab` — instructor hub: `https://manzo8b.github.io/risto-lab/`.
- `oiko` — household spending PWA: `https://manzo8b.github.io/oiko/`.
- `s-comodo` — independent blog: `https://manzo8b.github.io/s-comodo/`.
- `Torremolinos` — multilingual guide: `https://manzo8b.github.io/Torremolinos/`.
- `Lune_X` — artist site: `https://manzo8b.github.io/Lune_X/`.
- `README.md` — historical archive, do not confuse with the profile repository.

Private: six additional repositories. Their identities, source files and integrations must be reviewed privately; do not publish their inventory.

### Special risks

1. **GitHub Pages does not inherit the repository redirect.** Old `manzo8b.github.io` project URLs can stop working; new URLs should be `https://marcelo-fernandez.github.io/<repository>/` only after the new username takes effect.
2. **OIKO's IndexedDB content is origin-scoped.** Before the name change, export a backup of the free OIKO app using its built-in export; store it privately. A backup may contain sensitive personal-finance information, so do not upload it to GitHub. Test import on the new origin with a copy. TORREMOLINOS favorites and other local/browser storage are likewise origin-specific.
3. The GitHub profile README is displayed only when a public repo matches the account username. After renaming the account, rename `marcelo-fernandez/manzo8b` to `marcelo-fernandez/marcelo-fernandez` in repository **Settings → General → Repository name**.
4. Review OAuth callbacks, Supabase configuration, webhooks, app authorization settings, CORS/CSP, email templates, site origins, mobile shortcuts, and third-party tools (including DistroKid/streaming links) before claiming the migration complete. Do not expose the private OIKO Family project.
5. Search engines treat the new Pages host as a different address. After deploy, verify site ownership where relevant, update Search Console properties, resubmit sitemaps, inspect canonical/hreflang/Open Graph links and monitor indexing.
6. The MANZO AI `site-v0.7.zip` archive embeds site material. The workflow now includes a conditional text-asset URL rewrite **after** its source-integrity verification, preserving the ZIP. Run the workflow manually after the account change. Other projects may contain generated assets, compiled bundles and legacy hard-coded links that require separate review.
7. GitHub repository URLs may redirect, but old profile links, @mentions, gists, CODEOWNERS entries and certain GitHub noreply email commit verifications need manual checks.

## Phase 0 — before rename (safe now)

- Keep current live URLs unchanged.
- Record current repository list and recent successful GitHub Actions releases.
- Check GitHub 2FA and backup/export requirements; do not store credentials or exports in Git.
- Ensure a backup of critical local data, especially OIKO, **before** the old origin becomes inaccessible.
- This repository holds the helper at `scripts/post_rename_url_prs.py`. It only scans and creates reviewable pull requests; it does not merge.

## Phase 1 — account owner action (required)

1. Sign in to `https://github.com/settings/admin`.
2. Open **Change username**, read GitHub's warnings, and enter `marcelo-fernandez`.
3. Only if GitHub confirms availability, complete the username change. If unavailable, stop and choose a new candidate, then update the helper's `--new` value.
4. Confirm the new account URL and list all 15 repositories.
5. Immediately rename the special profile repository `manzo8b` to match the new username, so the public profile README continues to appear.

**The connected GitHub integration cannot execute account renames, edit repository settings or change pinned repositories. No automated step should claim these actions were completed.**

## Phase 2 — create *reviewable* URL PRs after rename

On a Mac, install/authenticate GitHub CLI (`gh`), Git and Python 3.10+. The helper uses only text files and leaves all ZIPs and media untouched.

**Before the account rename**, you may run a read-only inventory against the current profile repository:

```bash
gh auth login
gh repo clone manzo8b/manzo8b
cd manzo8b
python3 scripts/post_rename_url_prs.py --workdir ./audit-old
```

**After changing the username and renaming the profile repository**, clone the *new* profile repository into a fresh directory and run one of the following alternatives:

```bash
gh repo clone marcelo-fernandez/marcelo-fernandez
cd marcelo-fernandez

# Public repositories only: create reviewable PRs, never merge automatically.
python3 scripts/post_rename_url_prs.py --apply --workdir ./migration-public

# Alternatively, if private repos are also explicitly ready for review,
# run this INSTEAD of the public-only command (to avoid duplicate PRs):
# python3 scripts/post_rename_url_prs.py --apply --include-private --workdir ./migration-all
```

**Important:** `--apply` pushes branches and opens PRs; it does **not** merge them. Do not run both public and all-repo commands with duplicate PR branches unless the first batch is already reconciled. For review-only scanning after rename, use separate fresh work directories or inspect the generated PRs. The profile repository name must be updated before cloning the example above.

## Phase 3 — deploy and verify

Suggested order: MANZO AI → MARCELUS → RISTO-LAB → OIKO → S-COMODO → TORREMOLINOS → Lune_X.

Per site: review change diff, merge only when safe, run/check Pages action, open new URL on mobile/desktop, check navigation/search/forms/media, 404s, site manifests, RSS if present, robots/sitemap, alternate language links, search engine ownership, social previews, structured data. For OIKO, test local data migration with a *copy* of the exported backup and do not clear old browser storage. For cross-repository integrations update external callback URLs separately.

## Phase 4 — outbound profiles

Update GitHub profile links on LinkedIn, social bios, published portfolio, Buffer post templates, press kits, site footers, QR codes, email signatures and owned documentation. Do not promise that the old `github.io` host redirects. If long-term URL persistence is important, consider an owned custom domain and a dedicated redirect strategy, after verifying budget and ownership.

## References

- GitHub: https://docs.github.com/en/account-and-profile/concepts/username-changes
- Account rename UI: https://docs.github.com/en/account-and-profile/how-tos/account-management/changing-your-username
- Profile README: https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme
- GitHub Pages URLs: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
