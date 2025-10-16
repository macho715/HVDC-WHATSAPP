# Changelog

## [Unreleased] - 2025-01-16

### Added (PR #5: Storage State Management + Apify Dataset Push)

#### Storage State 관리
- AsyncGroupScraper에 `storage_state_path` 파라미터 추가로 Playwright 인증 상태 자동 로딩
- `_load_storage_state()` 메서드로 `auth.json` 자동 읽기 및 검증
- `_normalize_storage_state()` 정적 메서드로 레거시 쿠키 포맷 자동 변환 (리스트 → Playwright 표준 형식)
- ScraperSettings에 `auth_state_path` 필드 추가 (기본값: "auth.json")
- WhatsApp 로그인 타임아웃을 60초에서 120초로 증가
- 로그인 재시도 로직 추가 (최대 2회 시도, 페이지 리로드 포함)

#### Apify Dataset Push 통합
- ApifyDatasetClient 클래스 완전 재구현 (urllib 기반 HTTP 직접 구현)
- `ApifyDatasetClientError` 커스텀 예외 클래스 추가
- `_push_messages_to_dataset()` 비동기 메서드로 Apify dataset 자동 푸시
- 재시도 로직 (최대 3회, 지수 백오프: 1s → 2s → 4s)
- `save_messages()` 메서드에 dataset push 자동 통합
- GroupConfig에 `apify_dataset_id` 필드 지원

#### 설정 전파 및 통합
- MultiGroupManager에 `scraper_settings` 파라미터 추가
- `_create_scraper()`에서 `storage_state_path` 포함한 모든 설정 전달
- run_multi_group_scraper.py에서 `scraper_settings` 객체 직접 전달
- YAML 설정 파일에서 `auth_state_path` 및 `apify_dataset_id` 파싱 지원

#### 테스트 강화
- tests/test_async_scraper.py 신규 생성 (4개 테스트)
  - Apify dataset push 동작 검증
  - Storage state 로딩 검증
  - 레거시 포맷 정규화 검증
- tests/test_multi_group_scraper.py 업데이트
  - `auth_state_path` 검증 테스트 추가
  - `scraper_settings` 전파 테스트 추가
  - YAML 로드 시 신규 필드 파싱 검증

### Fixed
- WhatsApp Web 로그인 타임아웃 문제 해결 (storage state 자동 로딩)
- `auth.json` 레거시 포맷 호환성 문제 해결 (자동 정규화)
- 멀티 그룹 스크래핑 시 인증 실패 문제 개선 (재시도 로직)

### Technical Details
- **Commit**: `[FEAT] Apply PR #5: Storage state management + Apify dataset push` (4d28eac)
- **Files Changed**: 7 files, +484/-26 lines
- **Test Coverage**: 4 new tests in test_async_scraper.py, all passing
- **Code Quality**: Black, isort, flake8 validated

## [Previous Releases]
### Added
- WhatsApp auto extraction scheduler setup utility for Windows Task Scheduler.
- Tests covering scheduler file generation helpers.
- Optional Apify remote fallback pipeline for multi-group scraper failures.
- Logging of fallback execution results to `logs/multi_group_scraper.log`.

### Changed
- Updated extractor CLI to accept --run and --room aliases used in operational runbooks.
