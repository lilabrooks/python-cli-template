# Security policy

## Supported versions

This template tracks the current `main` branch. Released tags are kept for
history, but security fixes land on `main` first.

## Reporting a vulnerability

Please report security issues privately through GitHub Security Advisories for
this repository:

https://github.com/lilabrooks/python-cli-template/security/advisories/new

If GitHub advisories are unavailable, contact the maintainer through the email
listed in the repository's Git commit metadata. Please include:

- A short description of the issue.
- Steps to reproduce it.
- The affected files, commands, or generated-project path.
- Any known workaround.

Do not open a public issue for a vulnerability until there is a fix or a clear
disclosure plan.

## Scope

Security-sensitive areas include:

- `scripts/create-project` and `scripts/rename-project`, because they write
  files into user-selected paths.
- Generated-project setup and dependency installation paths.
- Provider adapters that touch credentials or model-provider SDKs.
- GitHub Actions and Dependabot configuration.

The template should never require checked-in secrets. Keep credentials in the
environment and use `.env.example` only as documentation.
