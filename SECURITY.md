# Security Policy

## Supported Versions

This project is a small educational desktop app. Security fixes are handled on the latest `main` branch unless release branches or tagged versions are introduced later.

| Version | Supported |
| --- | --- |
| `main` | Yes |
| older snapshots | No |

## Reporting a Vulnerability

If you find a vulnerability, please report it privately to the project maintainer instead of opening a public issue with exploit details.

Include:

- A clear description of the problem.
- Steps to reproduce it.
- The affected operating system and Python version.
- Any relevant logs, screenshots, or proof-of-concept details.
- Whether the issue requires local access, untrusted files, or network access.

Please do not include secrets, personal data, or unrelated machine details in a report.

## Security Scope

In scope:

- Unsafe local file handling.
- Dependency risks introduced by the project.
- Crashes or denial-of-service behavior caused by normal app input.
- Packaging or launch behavior that could execute unexpected code.

Out of scope:

- Issues in Python, Pygame, SDL, or operating system components unless this project uses them unsafely.
- Physical access attacks.
- Social engineering.
- Reports that only describe missing hardening for an offline educational app without a practical exploit path.

## Dependency Guidance

The runtime dependency is Pygame. Install it from the official Python package index or a trusted environment:

```powershell
python -m pip install pygame
```

Avoid running this project in an environment that contains sensitive secrets. The app does not need API keys, credentials, network access, or elevated permissions.

## Safe Development Practices

- Do not add network calls unless they are required and documented.
- Do not load or execute untrusted external files.
- Keep generated files such as `__pycache__` out of commits.
- Prefer deterministic, local simulation data over remote downloads.
- Review any new dependency before adding it.
