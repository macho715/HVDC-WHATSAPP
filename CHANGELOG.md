# Changelog

## [Unreleased]
### Added
- WhatsApp auto extraction scheduler setup utility for Windows Task Scheduler.
- Tests covering scheduler file generation helpers.
- Async scraper storage state loading with automatic normalization for Playwright
  compatibility.
- Configuration support for specifying auth storage files in multi-group YAML and
  propagation tests for scraper settings.

### Changed
- Updated extractor CLI to accept --run and --room aliases used in operational runbooks.
- Increased WhatsApp login tolerance and added retry handling when storage-backed
  sessions are unavailable during async scraping.

### Fixed
- Ensure the multi-group scraper CLI creates the logs directory before configuring logging
  handlers to avoid runtime crashes during tests and deployments.
