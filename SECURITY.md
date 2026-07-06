# Security Policy

## Supported versions

repoctx is pre-1.0; fixes land on the latest released minor version.

| Version | Supported |
| ------- | --------- |
| 0.3.x   | ✅        |
| < 0.3   | ❌        |

## Reporting a vulnerability

Please **do not** open a public issue for security problems.

Instead, use GitHub's private ["Report a vulnerability"][advisory] flow on this
repository, or email the maintainer. Include:

- a description of the issue and its impact,
- steps or a proof-of-concept to reproduce it,
- any suggested remediation.

You can expect an initial acknowledgement within a few days. Once a fix is
ready, it will be released and the report credited unless you prefer otherwise.

## Scope

repoctx runs locally and makes no network calls on its default path. The most
relevant surface is untrusted input to the parser and file walker; reports about
crashes, resource exhaustion, or path traversal there are especially welcome.

[advisory]: https://github.com/cwalker64/repoctx/security/advisories/new
