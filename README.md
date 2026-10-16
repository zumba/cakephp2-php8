# Fork of CakePHP 2 with support for PHP8

~~For original README content please check original repository: https://github.com/cakephp/cakephp/tree/2.x~~

Unfortunately branch 2.x in original repository was taken down.

## Zumba fork: PHP 8.5 branch (`cakephp2-php85`)

This repository (`zumba/cakephp2-php8`) is Zumba's fork of [kamilwylegala/cakephp2-php8](https://github.com/kamilwylegala/cakephp2-php8).
The `cakephp2-php85` branch is the version our applications use on PHP 8.5 containers. It contains:

- Every upstream fix up to and including the CSRF hardening (upstream #76), the PHP 8.4 fixes (#75, #83) and the PHP 8.5 fixes (#86).
- A CI matrix that runs the framework test suite on PHP 8.0, 8.1, 8.4 and 8.5. The test bootstrap converts every deprecation into a failure, so a green build means no deprecation notices on those versions.
- A local `docker/web` image based on `php:8.5-apache`.

The code stays compatible with PHP 8.0+; no PHP 8.5-only syntax is used.

### Requirements on PHP 8.5

- `ext-intl` must be installed in the container. `strftime()` was replaced by `IntlDateFormatter` (via `php81_bc/strftime`), which requires it.
- `ext-mcrypt` is no longer needed; `Security::encrypt()`/`decrypt()` use OpenSSL.

### Using the branch in an application

Point `composer.json` at this repository and at the branch:

```
{
	"require": {
		"cakephp/cakephp": "dev-cakephp2-php85 as 2.10.24"
	},
	"repositories": [
		{
			"type": "vcs",
			"url": "https://github.com/zumba/cakephp2-php8"
		}
	]
}
```

### Update procedure

Updating an application to the latest state of the branch is a standard composer update:

```
composer update cakephp/cakephp
```

Then run the application's own test suite under PHP 8.5. Commit the resulting `composer.lock`.

### Syncing new upstream fixes into the branch

1. `git fetch upstream` (where `upstream` is `https://github.com/kamilwylegala/cakephp2-php8.git`).
2. Bring the new upstream commits onto a feature branch cut from `cakephp2-php85` (merge or cherry-pick).
3. Run the test suite on PHP 8.5 (locally via `docker compose up` or by pushing and letting CI run the matrix).
4. Open a PR into `cakephp2-php85`.

## Why I created this fork? 🤔

CakePHP 2 stopped getting updates in the end of 2019 (AFAIR). Unfortunately in my case it's too expensive to migrate to newer versions of CakePHP. I started migrating to Symfony framework, but I still use ORM from CakePHP (and actually I like it). So in order to keep up with the newest PHP versions I decided to create fork of the framework.

## Why you should NOT use? ⛔

- Intention of this fork is to support PHP 8.*. Fork is not going to receive new features. Instead, fork is going to get minimal set of patches to comply with newer versions of PHP.
- If for example you're still on 5.6 or 7.0, you should **not** use this fork. Original `cakephp/cakephp` works perfectly fine on all PHP 7.* versions. You should migrate to newer versions of PHP and keep using original code. Once your application is battle tested on production I suggest migrating to PHP 8.

## When you could use this fork? ✅

Only prerequisite is to have your application already on PHP 7.4. Upgrade project to PHP 8.0 and replace CakePHP with this fork.

### Migration

Here are steps I took to migrate my project through all versions to PHP 8.1, maybe it can inspire you:

1. Decouple your tests from `CakeTestCase` and other utilities that are coupled to old PHPUnit version.
2. Once decoupled you can upgrade PHPUnit to the newest version accordingly to your PHP version.
3. Start upgrading gradually to newer versions of PHP. CakePHP 2 works perfectly fine on 7.0 - 7.4.
4. Once you're on 7.4 you can switch to 8 and this fork.

## Before using this fork ⚠️

- ~~Tests of CakePHP framework aren't refactored yet to support PHP 8. Main issue is old version of PHPUnit that is tightly coupled to framework's tests. Issue for fixing this situation is here: https://github.com/kamilwylegala/cakephp2-php8/issues/7~~ Framework tests are migrated to PHPUnit 9.*. Github actions are running tests on PHP 8.0, 8.1.
- ~~Due to lack of tests ☝️~~ - **you also need to rely** on tests in your application after integrating with this fork.
- If after integration you spot any issues related to framework please let me know by creating an issue or pull request with fix.

### Breaking changes

- In order to get rid of `strftime()` deprecation notices, it's required to switch to `IntlDateFormatter` class. This class is available in `intl` extension. Fork doesn't require it explicitly but to be able to use its functions Symfony ICU Polyfill is installed. To provide `strftime` behavior compatibility, `PHP81_BC\strftime` is used. `PHP81_BC` doesn't fully cover strftime, your code should work but there is a chance you'll get slightly different results. Discussed (here)[https://github.com/kamilwylegala/cakephp2-php8/pull/64] and (here)[https://github.com/kamilwylegala/cakephp2-php8/issues/65].

## Installation

This repository **is not** available in packagist, therefore your project's `composer.json` must be changed to point to custom repository.

Example configuration:
```
{
	"require": {
		"cakephp/cakephp": "dev-master as 2.10.24",
	},
	"repositories": [
        {
            "type": "vcs",
            "url": "https://github.com/kamilwylegala/cakephp2-php8"
        }
    ]
}
```

It means that composer will look at `master` branch of repository configured under `repositories` to resolve update of `cakephp/cakephp` package.

## Changelog

### 2026-10-16 (Zumba, branch `cakephp2-php85`)

- Synced all upstream fixes up to `kamilwylegala/cakephp2-php8` #87 (includes the CSRF fix #76 and the PHP 8.4/8.5 fixes #75, #83, #86).
- CI matrix now runs PHP 8.0, 8.1, 8.4 and 8.5; the test `app/Config/core.php` reports `E_ALL` so any deprecation fails the suite.
- PHP 8.5: `Security::cipher()` no longer casts the out-of-range `Security.cipherSeed` float to int (same seed value, no deprecation); `limit()`/`offset()` clamp out-of-range values instead of casting; `ConsoleLog` no longer calls `posix_isatty(null)`; `ReflectionProperty::setAccessible()` only on PHP < 8.1; null array offsets in `I18n`, `Helper`, `CakeResponse`, `ConsoleOptionParser`, `RequestHandlerComponent`, `Set`, `Configure`, `CakeSession` replaced by explicit checks; `libxml_disable_entity_loader()` calls removed.
- PHP 8.4: `trigger_error(..., E_USER_ERROR)` replaced by exceptions (`ConfigureException`, `CakeException`, `RuntimeException` in the webroot/console bootstrap scripts) or `ErrorHandler::handleFatalError()`.
- PHP 8.2: undeclared (dynamic) properties declared on `Scaffold`, `ConsoleOptionParser`, `HelpFormatter`, `MemcachedEngine`, `CakeTestCase`, `CakeTestFixture`, `CakeFixtureManager`, `ControllerTestDispatcher` and ~100 test classes; `ConnectionManager::create()` stores runtime connections on a `#[\AllowDynamicProperties]` subclass of `DATABASE_CONFIG`; `CakeRequest` allows dynamic properties.
- PHP 8.1: remaining "passing null to non-nullable internal parameter" cases fixed across the framework (strlen/strpos/strtolower/preg_*/trim/substr/… with `(string)` casts or null checks).
- `Security::encrypt()`/`decrypt()` fall back to OpenSSL when ext-mcrypt is missing.
- `SessionHandlerAdapter` methods marked `#[\ReturnTypeWillChange]`.
- Local `docker/web` image moved to `php:8.5-apache` (with `intl`, without `mcrypt`).

### 2025-02-04

- Fixes for PHP 8.4: `session_set_save_handler` accepts object, removed `E_STRICT` reference.
- Removed github action with php code sniffer. It's quite painful to work with. Need to migrate to something newer, that will affect code base as little as possible.

### 2024-11-16

- Inflector fix: str_place with null.

### 2024-09-21

- Added wrapper for PDOException to avoid creating dynamic property `queryString`.

### 2024-07-24

- Csrf vulnerabity fix back ported from Cake PHP 3
- Explicit type hint definition of nullable parameters.

### 2024-06-05

- Removed usage of `strftime`, replaced with Intl extension.

### 2024-05-24

- Fix deprecation error in Model: `Automatic conversion of false to array is deprecated`

### 2024-05-22

- Fix deprecation error in I18n: `Automatic conversion of false to array is deprecated`

### 2024-02-02

- `str_len` deprecation warning fix in CakeResponse (passing null instead of `string`)

### 2024-01-19

- `strotime()` and `preg_split()` in CakeResponse deprecation warning fixes (passing null)

### 2024-01-11

- `preg_replace` deprecation warning fixes (passing null instead of `string`)

### 2023-12-22

- `preg_quote()` passing null fix

### 2023-12-19

- Muted dynamic property creation warnings in Controller.php
- Fix passing a null input to h function (PR #56)
- Fix Hash class callback callable pattern deprecated (PR #58)

### 2023-11-13

- Silence dynamic property creation warning in Model.php

### 2023-11-02

- Fixed: unitialized property in Debugger.php

### 2023-10-20

- Fallback to empty string from `env()` in basics.php and request handler.

### 2023-10-19

- Removed usage of deprecated `redis->getKeys()` in favor of `redis->keys()`.
- Added docker-compose setup to run tests locally.

### 2023-09-18

- Fix for `ShellDispatcher` where `null` was passed to `strpos` function.

### 2023-08-18

- Fixed PHP8 deprecation notices. Related mostly to passing null as a `$haystack` value.

### 2023-06-02

- Fixed PHP 8.2 deprecation notices in CakeEvent: `Creation of dynamic property ... is deprecated.`

### 2023-02-19

- Fixed PHP 8.1 MySQL test suite.

### 2023-02-11

- Fixed PostgreSQL test suite.

### 2023-01-30

- `PaginatorHelper` fix.

### 2023-01-22

- Fixed views cache when relative time is specified.

### 2023-01-11

- Fixed test suite to run under PHPUnit 9.5 and PHP8. Big kudos to @tenkoma :clap:

### 2022-10-20

- `MailTransport` fix.

### 2022-10-08

- Support for `full_path` when uploading a file, PHP 8.1 only.

### 2022-09-27

- Fixed multiple `CREATE UNIQUE INDEX` statements from schema shell that did not work on PostgreSQL.

### 2022-03-08

- Fixed passing `params["pass"]` argument to `invokeArgs` when resolving controller action - `array_values` used to avoid problems with named parameters.

### 2022-03-03

- Removed `String` class.

### 2022-03-02

- Fixed `ConsoleErrorHandler::handleError` to respect error suppression.

### 2022-01-31

- Fixed `Folder->read`, `array_values` is used to remove keys to prevent usign named arguments in `call_user_func_array`

### 2022-01-16

- Fix Shell `ReflectionMethod::__construct` default null argument in hasMethod

### 2022-01-15

- Readme file update - more explicit content.

### 2022-01-04

- Fixed more deprecation notices
    - `strtoupper` + `converting false to array` in Mysql.php
    - `preg_match` where `$subject = null` in CakeRoute.php
    - `strtoupper` in DboSource.php
    - Check history for details ☝️


### 2021-12-20

- Fixed deprecation notices in PHP 8.1 for production code implementations:
    - `ArrayAccess`
    - `Countable`
    - `IteratorAggregate`
- PHP 8.0 requirement in composer.json
- **Warning:** Tests are not updated, Cake's tests rely on old version of PHPUnit so running them may show a lot of deprecations notices. Added issue to cover it: #7

### 2021-02-24

- Fixed ErrorHandler accordingly to PHP8 migration guide. Otherwise, error handler is logging too much and doesn't respect configured `error_reporting`.
