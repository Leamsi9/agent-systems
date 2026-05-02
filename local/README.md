# Local Agent Protocols

This directory is reserved for repo-local protocol extensions in consuming
repos.

The package installer creates `agent-protocols/local/` in target repos, but it
does not treat the directory as package-owned content:

- files in this directory are versioned by the consuming repo
- package refreshes must preserve local files here
- generic protocol improvements should be upstreamed to the package root
- repo-specific protocols should stay here

Do not add consumer-specific protocol files to the upstream package repo.
