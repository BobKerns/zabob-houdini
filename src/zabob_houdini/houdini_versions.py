#!/usr/bin/env uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "click",
#     "requests",
#     "semver",
#     "python-dotenv",
#     "charset-normalizer<3.4.0",
# ]
# ///


from collections.abc import Mapping, Collection
from functools import reduce
import os
from platform import uname
import json
from pathlib import Path
import re
from typing import Any, Final, Literal, TypedDict, cast
import sys
import time
from datetime import datetime
from collections import defaultdict

import requests
import click
from semver import Version
# Add dotenv support
from dotenv import load_dotenv

load_dotenv()  # Load from .env if available]

HOUDINI_FALLBACK_VERSION: Final[Version] = Version.parse(os.getenv("HOUDINI_FALLBACK_VERSION", "20.5.584"))
HOUDINI_DEFAULT_MIN_VERSION: Final[Version] = Version(20, 5)
HOUDINI_VERSIONS_CACHE_NAME: Final[str] = "houdini_versions_cache.json"
HOUDINI_DEFAULT_CACHE_DIR: Final[Path] = Path(os.getenv("CACHE_DIRECTORY", Path.home() / '.houdini-cache'))
HOUDINI_VERSIONS_CACHE: Final[Path] = HOUDINI_DEFAULT_CACHE_DIR / HOUDINI_VERSIONS_CACHE_NAME
HOUDINI_INSTALLERS_DIR: Final[Path] = HOUDINI_DEFAULT_CACHE_DIR / "installers"


type Architecture = Literal['arm64', 'x86_64']
type PlatformUI= Literal['linux', 'windows', 'macos']
type PlatformSFX= Literal['linux', 'win', 'macosx', 'macosx_arm64']
type Platform= Literal['linux', 'Windows', 'Darwin']
type BuildType = Literal['gcc9.3', 'gcc11.2', 'gcc12.2']|str

_OS: Final[Platform] = cast(Platform, uname().system)
_ARCH: Final[Architecture] = cast(Architecture, uname().machine)


class SemVerParamType(click.ParamType):
    """Provide a custom click type for semantic versions.

    This custom click type provides validity checks for semantic versions.
    """
    name = 'semver'
    _min_parts: int = 3
    _max_parts: int = 3

    _min_version: Version|None = None
    _max_version: Version|None = None

    def __init__(self,
                 min_parts: int = 3,
                 max_parts: int = 3,
                 min_version: Version|None = None,
                 max_version: Version|None = None,
    ) -> None:
        """
        Initialize the SemVerParamType.

        :param min_parts: If True, the minor version is optional.
        :type min_parts: int
        :param max_parts: If True, the patch version is optional.
        :type max_parts: int
        :param min_version: The minimum version allowed.
        :type min_version: semver.Version|None
        :param max_version: The maximum version allowed.
        :type max_version: semver.Version|None
        """
        super().__init__()
        self._min_parts = min(min_parts, max_parts)
        self._max_parts = max(max_parts, min_parts)
        self._min_version = min_version
        self._max_version = max_version


def _version(version: Version|str) -> Version:
    """
    Convert a version to a semver.Version object.

    Args:
        version (Version|str): The version to convert.

    Returns:
        Version: The converted version.
    """
    if isinstance(version, Version):
        return version
    return Version.parse(version, optional_minor_and_patch=True)


    def convert(self, value: str, param: Parameter|None, ctx: Context|None) -> Version:
        """Converts the value from string into semver type.

        This method takes a string and check if this string belongs to semantic version definition.
        If the test is passed the value will be returned. If not a error message will be prompted.

        :param value: the value passed
        :type value: str
        :param param: the parameter that we declared
        :type param: str
        :param ctx: context of the command
        :type ctx: str
        :return: the passed value as a checked semver
        :rtype: str
        """
        parts = value.count('.') + 1
        if parts > self._max_parts:
            segments = ('major', 'minor', 'patch', 'prerelease', 'build')
            expect = '.'.join(segments[:self._max_parts])
            self.fail(f"Not a valid version, expected at most {expect}", param, ctx)
        elif parts < self._min_parts:
            segments = ('major', 'minor', 'patch', 'prerelease', 'build')
            expect = '.'.join(segments[:self._min_parts])
            self.fail(f"Not a valid version, expected at least {expect}", param, ctx)
        else:
            try:
                result = _version(value)
                if self._min_version and self._max_version:
                    if result > self._max_version or result < self._min_version:
                        self.fail(f"Version {result} is not in range {self._min_version} - {self._max_version}",
                                  param,
                                  ctx)
                if self._min_version and result < self._min_version:
                    self.fail(f"Version {result} is less than minimum version {self._min_version}",
                              param,
                              ctx)
                if self._max_version and result > self._max_version:
                    self.fail(f"Version {result} is greater than maximum version {self._max_version}",
                              param,
                              ctx)
                return result
            except ValueError as e:
                self.fail('Not a valid version, {0}'.format(str(e)), param, ctx)


def platform_ui(name: PlatformSFX|Platform|PlatformUI=_OS) -> PlatformUI:
    """Convert platform from SFX or OS to UI format."""
    lower = name.lower()
    match lower:
        case 'darwin'|'macosx'|'macosx_arm64'|'macos':
            return 'macos'
        case 'win'|'windows':
            return 'windows'
        case 'linux':
            return 'linux'
        case _:
            raise ValueError(f"Unknown platform: {name}")

def platform_sfx(name: PlatformUI|Platform=_OS, arch: Architecture=_ARCH) -> PlatformSFX:
    """Convert platform from UI or OS to SFX format."""
    lower = name.lower()
    match lower:
        case 'macos'|'darwin'|'macosx'|'macosx_arm64':
            if arch == 'arm64':
                return 'macosx_arm64'
            return 'macosx'
        case 'linux':
            return 'linux'
        case 'windows'|'win':
            return 'win'
        case _:
            raise ValueError(f"Unknown platform: {name}")

class VersionedSFX(TypedDict):
    """Side Effects version information."""
    version: str
    build: str


class VersionExtended(TypedDict):
    build: int
    architecture: Architecture
    build_type: BuildType

class Versioned(TypedDict):
    version: Version
    full_version: Version

class VersionedJSON(TypedDict):
    version: str
    full_version: str


class BaseSFXBuildInfo(TypedDict):
    """Build information for SideFX Houdini."""
    id: int
    product: str
    release: str
    display_name: str
    package_exists: bool
    hash: str #Sha256
    download_url: str
    hash_pdb: bool
    pdb_url: str
    bad_quality: bool
    size: int
    is_launcher: bool

class SFXBuildInfo(BaseSFXBuildInfo, VersionedSFX):
    """Build information for SideFX Houdini."""
    os: PlatformSFX


class BuildInfo(BaseSFXBuildInfo, Versioned, VersionExtended):
    """Build information for Houdini."""
    os: PlatformUI

class JSONBuildInfo(BaseSFXBuildInfo, VersionedJSON, VersionExtended):
    """Build information for Houdini in JSON format."""
    os: PlatformUI


class VersionJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for Version objects."""
    def default(self, o: Any):
        if isinstance(o, Version):
            return str(o)
        return super().default(o)

_RE_BUILD_TYPE = re.compile(r"_(arm64|x86_64)(?:_(.+))?\.(?:dmg|tar.gz|exe|zip)$")
_RE_BUILD_TYPE_WIN = re.compile(r"-(win64)(?:-(.+))?\.exe$")

def enliven_build(info: SFXBuildInfo|JSONBuildInfo) -> BuildInfo:
    """Convert a SFXBuildInfo or JSONBuildInfo to a BuildInfo."""
    # Convert the build to a BuildInfo
    version = Version.parse(info["version"], optional_minor_and_patch=True)
    build = int(info["build"])
    full_version=Version(version.major, version.minor, build)
    display_name = info["display_name"]
    platform = platform_ui(info["os"])
    architecture = info.get("architecture", None)
    build_type = info.get("build_type", None)
    if architecture is None and platform == "windows":
        architecture = "x86_64"
    if architecture is None or build_type is None:
        m = (_RE_BUILD_TYPE.search(display_name)
             or _RE_BUILD_TYPE_WIN.search(display_name))
        if m:
            architecture = architecture or m.group(1)
            build_type = build_type or m.group(2) or ''
        else:
            architecture = architecture or ''
            build_type = build_type or ''

    return BuildInfo(
                full_version=full_version,
                version=version,
                build=build,
                architecture=cast(Architecture, architecture),
                build_type=cast(BuildType, build_type),
                os=platform,
                **{
                    key: value
                    for key, value in info.items()
                    if key not in ('version', 'full_version', 'build', 'architecture', 'build_type', 'os')
                }) # type: ignore


def is_build_good(build: SFXBuildInfo) -> bool:
    """Check if the build is good based on its quality."""
    return bool(
        # Make sure the package exists
        build.get("package_exists") and
        # Not marked as bad quality
        not build.get("bad_quality")
    )

def read_cache_file(cache_file: Path) -> Mapping[Version, Collection[BuildInfo]]|None: # Check cache age
    if cache_file.exists():
        cache_age_hours = 0
        try:
            mtime = os.path.getmtime(cache_file)
            cache_age_hours = (time.time() - mtime) / 3600
        except Exception as e:
            print(f"Failed to get cache file modification time: {e}", file=sys.stderr)
            return None

        # Use cache if it's less than 24 hours old
        if cache_age_hours < 24:
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                    cached_versions: dict[str, list[JSONBuildInfo]] = cached_data.get("versions", [])
                    # Filter cached versions by minimum
                    return {
                        Version.parse(release): [enliven_build(build) for build in builds]
                        for release, builds in cached_versions.items()
                    }
            except Exception as e:
                print(f"Failed to read cache file: {e}", file=sys.stderr)
                # if cache is corrupted, delete it
                cache_file.unlink(missing_ok=True)
                return None
    return None


def _group_by_major_minor(
    builds: Collection[BuildInfo],
) -> Mapping[Version, Collection[BuildInfo]]:
    """
    Group specific versions by major.minor release version.
    """
    def by_major_minor(a: Mapping[Version, list[BuildInfo]],
                       i: BuildInfo,
                       ) -> Mapping[Version, list[BuildInfo]]:
        v = i["full_version"]
        release = Version(v.major, v.minor)
        a[release].append(i)
        return a
    return reduce(by_major_minor,
                builds,
                defaultdict(list))


def get_version_ranges(
    min_version: Version|None=HOUDINI_DEFAULT_MIN_VERSION,
    cache_file: Path=HOUDINI_VERSIONS_CACHE,
    session: requests.Session|None=None,
    ) -> Mapping[Version, Collection[BuildInfo]]:
    """Get oldest and newest builds for each major.minor release using authenticated API."""

    def filter_builds(builds: Collection[BuildInfo]) -> Collection[BuildInfo]:
        return [
            build
            for build in builds
            if min_version is None or build["full_version"] >= min_version
        ]

    def filter_releases(releases: Mapping[Version, Collection[BuildInfo]]) -> Mapping[Version, Collection[BuildInfo]]:
        return {
                release: filtered_builds
                for release, filtered_builds in (
                                (release, filter_builds(builds))
                                for release, builds in releases.items()
                            )
                if filtered_builds
            }

    # Check if we should use cache first (for GitHub Actions)
    if os.environ.get("CACHE_HIT", "true") == "true":
        # Check cache age
        cached = read_cache_file(cache_file)
        if cached is not None:
            return filter_releases(cached)

    if not session:
        # Login first using credentials from environment
        session = login_session(requests.Session())

    try:
        # Get the build list
        build_resp = session.get("https://www.sidefx.com/download/daily-builds/get/")

        if build_resp.status_code != 200:
            raise RuntimeError(f"Failed to get build list: {build_resp.status_code}")

        # Try to parse the JSON response
        try:
            build_data = build_resp.json()
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON response: {e}") from e

        # Check in daily_builds_releases
        releases: list[SFXBuildInfo] = build_data.get("daily_builds_releases", [])
        production_builds = [
            enliven_build(build)
            for build in releases
            if is_build_good(build)
            for version in (
                Version.parse(build.get("version"),
                              optional_minor_and_patch=True),
            )
            for patch in (int(build.get("build")),)
        ]

        version_groups = _group_by_major_minor(production_builds)

        # Cache the results
        if cache_file:
            try:
                with open(cache_file, 'w') as f:
                    # Include metadata about when cache was created
                    cache_data = {
                        "versions": {str(k):v for k,v in version_groups.items()},
                        "cache_date": datetime.now().isoformat(),
                        "min_version": min_version
                    }
                    json.dump(cache_data, f, cls=VersionJsonEncoder, indent=4)
            except Exception as e:
                print(f"Failed to write cache: {e}", file=sys.stderr)

        return version_groups

    except Exception as e:
        raise RuntimeError(f"Error fetching versions: {e}") from e


def test_versions(min_version: Version|None=None,):
    env_versions = os.environ.get("HOUDINI_TEST_VERSIONS")
    if env_versions:
        versions = env_versions.split(",")
        # Parse, then filter versions based on minimum
        return [
            v
            for v in (
                Version.parse(vstr)
                for vstr in versions
            )
            if min_version is None or v >= min_version
        ]
    def build_version(build: BuildInfo) -> Version:
        return build["full_version"]

    version_groups = get_version_ranges()
    # For each major.minor, select oldest and newest
    test_ranges = {
        v: (
            min(builds,key=build_version),
            max(builds,key=build_version)
        )
        for v, builds in version_groups.items()
    }
    return sorted(set(test_ranges.values()))


def find_build(
    version: Version,
    platform: PlatformUI=platform_ui(),
    arch: Architecture=_ARCH,
    build_type: BuildType="",
    session: requests.Session|None=None,
) -> BuildInfo|None:
    """
    Find a specific Houdini build.

    Args:
        version: Full version of Houdini to find (e.g. 20.5.584)
        platform: Platform to find for (linux, windows, macos)
        arch: CPU architecture (arm64 or x86_64)
        build_type: Build type (gcc9.3, gcc11.2, etc)
        session: Optional requests session for authentication
    Returns:
        BuildInfo object if found, None otherwise
    """

    release = Version(version.major, version.minor)
    builds_map = get_version_ranges(session=session)
    builds= builds_map.get(release, [])
    if not builds:
        return None
    for build in builds:
        # Check if the build matches the requested platform, arch, and build type
        if (
            build["os"] == platform and
            not build_type or build["build_type"] == build_type and
            build["architecture"] == arch and
            build["full_version"] == version
        ):
            return build


def get_houdini_builds():
    pass


def download_houdini_installer(version: Version,
                               platform: PlatformUI=platform_ui(),
                               arch: Architecture=_ARCH,
                               build_type: BuildType="",
                               session: requests.Session|None=None,
                               ) -> Path:
    """
    Download a specific Houdini installer.

    Args:
        version: Version of Houdini to download (e.g. 20.5.584)
        platform: Platform to download for (linux, windows, macos)
        arch: CPU architecture (arm64 or x86_64)
        build_type: Build type (gcc9.3, gcc11.2, etc)
        session: Optional requests session for authentication
    Returns:
        Path to the downloaded installer file
    """
    if not session:
        # Login first using credentials from environment
        session = login_session(requests.Session())

    if version.patch == 0:
        raise ValueError("Patch (Houdini build) version must be specified (e.g. 20.5.584)")

    build = find_build(version,
                       platform=platform,
                       arch=arch,
                       build_type=build_type,
                       session=session)
    if not build:
        click.echo(f"Build not found for version {version} on {platform} ({arch}, {build_type})",
                    file=sys.stderr)
        sys.exit(2)

    # Create download URL
    download_url = f"https://www.sidefx.com/{build['download_url']}"

    # Create cache directory
    download_dir = Path(os.getenv("HOUDINI_DOWNLOAD_DIR", HOUDINI_DEFAULT_CACHE_DIR / "installers"))
    download_dir.mkdir(exist_ok=True, parents=True)
    output_name = build['display_name']

    # Output file path
    output_file = download_dir / output_name

    # Skip if file already exists
    if output_file.exists():
        print(f"Installer already exists: {output_file}", file=sys.stderr)
        return output_file

    print(f"Downloading Houdini {version} for {platform}_{arch}...", file=sys.stderr)

    # Stream download to file with progress indicator
    with session.get(download_url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        downloaded = 0
        with open(output_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                # Show progress
                if total_size > 0:
                    done = int(50 * downloaded / total_size)
                    sys.stderr.write(f"\r[{'=' * done}{' ' * (50-done)}] {downloaded/1024/1024:.1f}/{total_size/1024/1024:.1f} MB")
                    sys.stderr.flush()

        if total_size > 0:
            sys.stderr.write("\n")

    print(f"Downloaded to: {output_file}", file=sys.stderr)
    return output_file

def login_session(session: requests.Session) -> requests.Session:
    """Login to SideFX using environment credentials."""
    # Get credentials from environment
    username = os.environ.get("SIDEFX_USERNAME")
    password = os.environ.get("SIDEFX_PASSWORD")

    if not username or not password:
        raise ValueError("SIDEFX_USERNAME and SIDEFX_PASSWORD must be set (via environment or .env file)")

    # Common browser-like headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.sidefx.com/login/",
        "Connection": "keep-alive"
    }

    session.headers.update(headers)

    # First get the login page to obtain CSRF token
    login_page = session.get("https://www.sidefx.com/login/")

    # Add a small delay
    time.sleep(1)

    # Prepare login data
    login_data = {
        "username": username,
        "password": password,
        "next": "/download/daily-builds/get/"
    }

    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text)
    if csrf_match:
        login_data["csrfmiddlewaretoken"] = csrf_match.group(1)
        session.headers.update({"Referer": "https://www.sidefx.com/login/"})

    # Perform login
    login_resp = session.post(
        "https://www.sidefx.com/login/",
        data=login_data,
        allow_redirects=True
    )

    if login_resp.status_code != 200:
        raise Exception(f"Login failed: {login_resp.status_code}")

    time.sleep(1)  # Add a small delay after login
    return session

# Create a click group as the main entry point
@click.group()
def cli():
    """Houdini version management tools."""
    pass

# First subcommand - get versions
@cli.command('versions')
@click.option('--cache-dir',
              default=os.getenv("HOUDINI_VERSIONS_CACHE",
                                HOUDINI_DEFAULT_CACHE_DIR),
              help='Directory to cache Houdini versions.')
@click.option('--min-version',
            metavar='VERSION',
            type=SemVerParamType(min_parts=2),
            default=os.getenv("HOUDINI_MIN_VERSION",
                            str(HOUDINI_DEFAULT_MIN_VERSION)),
            help='Minimum Houdini version to consider.')
@click.option('--platforms', multiple=True,
              type=click.Choice(['linux', 'windows', 'macos'], case_sensitive=False),
              default=os.getenv("HOUDINI_PLATFORMS", platform_ui()).split(','),
              help='Platforms to filter (linux, windows, macos).')
@click.option('--products', multiple=True,
              type=str,
              metavar='PRODUCT|*',
              default=os.getenv("HOUDINI_PRODUCTS", 'houdini').split(','),
              help='Products to filter (houdini, hengine).')
@click.option('--architectures', multiple=True,
              type=click.Choice(['arm64', 'x86_64'], case_sensitive=False),
              default=os.getenv("HOUDINI_ARCHITECTURES", _ARCH).split(','),
              help='Architectures to filter (arm64, x86_64).')
@click.option("--dev", "dev",
              is_flag=True,
              default=False,
              help="Includes development versions.")
def versions_command(
        cache_dir: Path|str=HOUDINI_VERSIONS_CACHE,
        min_version: Version|None=None,
        platforms: Collection[PlatformUI]=(platform_ui(),),
        products: Collection[str]=('houdini',),
        architectures: Collection[Architecture]=(_ARCH,),
        dev: bool=False,
    ):
    """Get Houdini versions for testing."""
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(exist_ok=True, parents=True)
    cache_file = cache_dir / Path(HOUDINI_VERSIONS_CACHE_NAME).name

    # Get versions
    versions = get_version_ranges(min_version, cache_file)
    for release, builds in versions.items():
        print(f"{release}:")
        for build in builds:
            product = build["product"]
            os_ = build["os"]
            arch = build["architecture"]
            if product not in products and '*' not in products:
                continue
            if os_ not in platforms:
                continue
            if arch not in architectures:
                continue
            if not dev and build["release"] != "gold":
                continue
            print(f"  - {build['full_version']} [{product}] ({os_}/{arch}/{build['build_type']})")

@cli.command('download')
@click.argument('version',
              type=SemVerParamType(),
              default=os.getenv("HOUDINI_VERSION",
                                str(HOUDINI_FALLBACK_VERSION)))
@click.option('--arch',
            type=click.Choice(['arm64', 'x86_64'], case_sensitive=False),
            default=os.getenv("HOUDINI_ARCH", _ARCH),
            help='CPU architecture (arm64 or x86_64).')
@click.option('--build-type',
            default=os.getenv("HOUDINI_BUILD_TYPE", ""),
            help='Build type (gcc9.3, gcc11.2, etc).')
@click.option('--output-path',
            type=click.Path(exists=False, dir_okay=False),
            help='Path to save the downloaded file (for Docker integration).')
@click.option('--credentials',
            type=click.Path(exists=True, dir_okay=False),
            help='Path to .env file with SIDEFX_USERNAME and SIDEFX_PASSWORD')
def download_command(version: Version=HOUDINI_FALLBACK_VERSION,
                   arch: Architecture="arm64",
                   build_type: BuildType="",
                   output_path: Path|None=None,
                   credentials: Path|None=None,
                ):
    """Download a Houdini installer."""
    try:
        # Load credentials file if provided
        if credentials:
            load_dotenv(dotenv_path=credentials, override=True)

        session = requests.Session()
        login_session(session)
        # Rest of your download code...
        installer_path = download_houdini_installer(
            version=version,
            arch=arch,
            build_type=build_type,
            session=session
        )

        # If output path is specified, copy there (for Docker build)
        if output_path:
            import shutil
            output_path = Path(output_path)
            output_path.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy2(installer_path, output_path)
            print(f"Copied to: {output_path}", file=sys.stderr)

        # Print the path to stdout for capturing in scripts
        print(installer_path)
    except Exception as e:
        print(f"Error downloading Houdini: {e}", file=sys.stderr)
        sys.exit(1)


@cli.command('show')
@click.argument('version', type=SemVerParamType())
@click.option('--platform',
              type=click.Choice(['linux', 'windows', 'macos'], case_sensitive=False),
              default=os.getenv("HOUDINI_PLATFORM", platform_ui()),
              help='Platform to show (linux, windows, macos).')
@click.option('--arch',
              type=click.Choice(['arm64', 'x86_64'], case_sensitive=False),
              default=os.getenv("HOUDINI_ARCH", _ARCH),
              help='CPU architecture (arm64 or x86_64).')
@click.option('--build-type',
              default=None,
              help='Build type (gcc9.3, gcc11.2, etc).')
def show_command(version: Version,
                 platform: PlatformUI=platform_ui(),
                 arch: Architecture=_ARCH,
                 build_type: BuildType=""):
    """Show Houdini build information."""
    build = find_build(version, platform=platform, arch=arch, build_type=build_type)
    if build:
        name = build['display_name']
        cache_dir = Path(os.getenv("HOUDINI_DOWNLOAD_DIR", HOUDINI_DEFAULT_CACHE_DIR / "installers"))
        cache_dir.mkdir(exist_ok=True, parents=True)
        cache_file = cache_dir / name
        def info(label, value):
            print(f' . {label:<15} {value}')
        info("Build found", build['full_version'])
        info("Product", build['product'])
        info("Platform", build['os'])
        info('Architecture', build['architecture'])
        if build['build_type']:
            info('Library type', build['build_type'])
        info("Download URL", f"https://www.sidefx.com/{build['download_url']}")
        info("File name", name)
        info("Size", f"{build['size']:,d} bytes")
        info("HASH", build['hash'])
        if cache_file.exists():
            info("Status",  "Downloaded")
        else:
            info("Status", "Available")
    else:
        print(f"No build found for version {version} on {platform} ({arch}, {build_type})", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    cli()  # Use the cli group instead of main function
