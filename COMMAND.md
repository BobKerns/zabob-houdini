![Zabob Banner](docs/images/zabob-banner.jpg)
# Zabob-Houdini Command Line Interface

Zabob-Houdini provides a comprehensive CLI for development, testing, and integration with Houdini. The CLI automatically bridges between regular Python and Houdini's Python environment (`hython`) when needed.

## Installation and Setup

```bash
# Install the package
pip install zabob-houdini

# Install as a Houdini package (optional)
python -m zabob_houdini install-package
```

## Global Options

All commands support:
- `--version`: Show version and exit
- `--help`: Show help message and exit

## Main Command Structure

```text
zabob-houdini [OPTIONS] COMMAND [ARGS]...
```

The CLI provides several command groups and individual commands for different aspects of Houdini development and integration.

## Command Groups

### `info` - Houdini Environment Information

Extract detailed information about the Houdini environment and node types.

```bash
python -m zabob_houdini info [COMMAND]
```

#### `info categories`
Analyze node categories in the current Houdini session.

```bash
python -m zabob_houdini info categories [ARGS...]
```

**Usage:**
- Analyzes all available node categories in Houdini
- Outputs category hierarchy and relationships
- Requires Houdini environment (automatically uses `hython`)

#### `info types CATEGORY`
List node types in the specified category with detailed information.

```bash
python -m zabob_houdini info types CATEGORY
```

**Arguments:**
- `CATEGORY`: The name of the node category to analyze (e.g., 'sop', 'object', 'dop')

**Example Output:**
```text
Node types in category 'Sop' (Geometry):

NAME                    DESCRIPTION              INPUTS   OUTPUTS  IN CATEGORIES           FLAGS
------------------------------------------------------------------------------------------------
add                     Add                      0-1      1        -                       GENERATOR
agent                   Agent                    0-1      1        -
blend                   Blend                    0-9999   1        Chop, Cop, Cop2, Dop...
box                     Box                      0        1        -                       GENERATOR
```

**Features:**
- Shows node name, description, input/output counts
- "IN CATEGORIES" column shows which parent categories can contain each node
- FLAGS column shows special properties (GENERATOR, MANAGER, DEPRECATED)
- Table formatting with appropriate column widths
- Requires Houdini environment (automatically uses `hython`)

---

### `houdini` - Houdini Version Management

Tools for managing Houdini installations and versions.

```bash
python -m zabob_houdini houdini [COMMAND]
```

#### `houdini versions`
Get available Houdini versions for testing and development.

```bash
python -m zabob_houdini houdini versions [OPTIONS]
```

**Options:**
- `--cache-dir PATH`: Directory to cache Houdini versions (default: from `HOUDINI_VERSIONS_CACHE` env var)
- `--min-version VERSION`: Minimum Houdini version to consider (default: from `HOUDINI_MIN_VERSION` env var or 21.0)
- `--platforms [linux|windows|macos]`: Platforms to filter (multiple allowed, default: current platform)
- `--products PRODUCT`: Products to filter (houdini, hengine, default: houdini)
- `--architectures [arm64|x86_64]`: Architectures to filter (multiple allowed, default: current arch)
- `--dev`: Include development versions (default: False)

**Environment Variables:**
- `HOUDINI_VERSIONS_CACHE`: Cache directory path
- `HOUDINI_MIN_VERSION`: Minimum version to consider
- `HOUDINI_PLATFORMS`: Comma-separated list of platforms
- `HOUDINI_PRODUCTS`: Comma-separated list of products
- `HOUDINI_ARCHITECTURES`: Comma-separated list of architectures

#### `houdini download VERSION`
Download a Houdini installer.

```bash
python -m zabob_houdini houdini download VERSION [OPTIONS]
```

**Arguments:**
- `VERSION`: Houdini version to download (default: from `HOUDINI_VERSION` env var)

**Options:**
- `--arch [arm64|x86_64]`: CPU architecture (default: from `HOUDINI_ARCH` env var or current arch)
- `--build-type TEXT`: Build type like gcc9.3, gcc11.2 (default: from `HOUDINI_BUILD_TYPE` env var)
- `--output-path PATH`: Path to save the downloaded file
- `--credentials PATH`: Path to .env file with SIDEFX_USERNAME and SIDEFX_PASSWORD

**Environment Variables:**
- `HOUDINI_VERSION`: Default version to download
- `HOUDINI_ARCH`: Default architecture
- `HOUDINI_BUILD_TYPE`: Default build type

#### `houdini show VERSION`
Show detailed information about a specific Houdini build.

```bash
python -m zabob_houdini houdini show VERSION [OPTIONS]
```

**Arguments:**
- `VERSION`: Houdini version to show information for

**Options:**
- `--platform [linux|windows|macos]`: Platform to show (default: from `HOUDINI_PLATFORM` env var or current platform)
- `--arch [arm64|x86_64]`: CPU architecture (default: from `HOUDINI_ARCH` env var or current arch)
- `--build-type TEXT`: Build type (default: auto-detected)

**Example Output:**
```text
 . Build found     21.0.512
 . Product         houdini
 . Platform        macos
 . Architecture    arm64
 . Download URL    https://www.sidefx.com/...
 . File name       houdini-21.0.512-macosx_arm64.dmg
 . Size            2,456,789,012 bytes
 . HASH            sha256:abc123...
 . Status          Available
```

---

### `diagnostics` - Environment Testing

Commands for testing Houdini integration and functionality.

```bash
python -m zabob_houdini diagnostics [COMMAND]
```

#### `diagnostics test-node`
Test creating a simple node (requires Houdini).

```bash
python -m zabob_houdini diagnostics test-node
```

**Features:**
- Tests basic node creation functionality
- Validates Houdini Python environment integration
- Uses the hython bridge automatically
- Reports success/failure with detailed information

#### `diagnostics test-chain`
Test chain functionality.

```bash
python -m zabob_houdini diagnostics test-chain
```

**Features:**
- Tests zabob-houdini's chain creation capabilities
- Validates the chain API works correctly
- Uses the hython bridge automatically

---

## Individual Commands

### `environment`
Display comprehensive Python and Houdini environment information.

```bash
python -m zabob_houdini environment
```

**Output includes:**
- Python version and executable path
- Platform information
- Houdini availability status
- Houdini application version and build
- Environment variables (HOUDINI_PATH, PYTHONPATH)
- Path listings for development

**Example Output:**
```text
Environment Information:
==================================================
Python Version: 3.11.5
Python Executable: /usr/local/bin/python3.11
Platform: darwin
Houdini Available: true

Houdini Information:
------------------------------
Application: Houdini
Version: 21.0.512
Build: 512
Hython Version: 3.11.5
HOUDINI_PATH:
  /Users/user/houdini21.0
  /Applications/Houdini/Frameworks/Houdini.framework/Versions/21.0.512/Resources/houdini
```

### `validate`
Validate Houdini installation and Python environment.

```bash
python -m zabob_houdini validate
```

**Features:**
- Quick validation of Houdini environment
- Returns exit code 0 for success, 1 for failure
- Useful for CI/CD pipelines and scripts

### `list-types`
List available Houdini node types (legacy command).

```bash
python -m zabob_houdini list-types [OPTIONS]
```

**Options:**
- `--category, -c [sop|obj|dop|cop|vop|top]`: Filter by node category

**Note:** This is a legacy command. Use `info types` for enhanced formatting and features.

### `install-package`
Install zabob-houdini as a Houdini package.

```bash
python -m zabob_houdini install-package
```

**Features:**
- Installs zabob-houdini into Houdini's package system
- Makes the package available in Houdini Python nodes and shelf tools
- Checks for proper permissions and Houdini installation

### `uninstall-package`
Remove zabob-houdini Houdini package.

```bash
python -m zabob_houdini uninstall-package
```

**Features:**
- Removes zabob-houdini from Houdini's package system
- Clean removal of package files

## Advanced Usage

### Environment Variables

The CLI supports several environment variables for configuration:

**Houdini Version Management:**
- `HOUDINI_VERSION`: Default Houdini version for downloads
- `HOUDINI_FALLBACK_VERSION`: Fallback version (default: 21.0.512)
- `HOUDINI_MIN_VERSION`: Minimum version to consider (default: 21.0)
- `HOUDINI_PLATFORM`: Target platform (linux/windows/macos)
- `HOUDINI_ARCH`: Target architecture (arm64/x86_64)
- `HOUDINI_BUILD_TYPE`: Build type (gcc9.3, gcc11.2, etc.)

**Caching:**
- `HOUDINI_VERSIONS_CACHE`: Cache directory for version data
- `HOUDINI_DOWNLOAD_DIR`: Directory for downloaded installers
- `CACHE_DIRECTORY`: General cache directory (default: ~/.houdini-cache)

**Authentication:**
- `SIDEFX_USERNAME`: SideFX account username for downloads
- `SIDEFX_PASSWORD`: SideFX account password for downloads

### Bridge Architecture

The CLI uses a sophisticated bridge architecture that automatically dispatches commands between regular Python and Houdini's Python environment (`hython`) as needed:

- **Regular Python commands**: Environment info, version management, validation
- **Houdini-specific commands**: Node analysis, type listings, functionality tests
- **Automatic dispatch**: Commands marked with `@houdini_command` automatically run via `hython`
- **JSON communication**: Results passed via JSON between environments

### Integration Examples

**CI/CD Pipeline:**
```bash
# Validate environment
python -m zabob_houdini validate

# Check available Houdini versions
python -m zabob_houdini houdini versions --min-version 21.0

# Test functionality
python -m zabob_houdini diagnostics test-node
```

**Development Workflow:**
```bash
# Check environment
python -m zabob_houdini environment

# Install as Houdini package
python -m zabob_houdini install-package

# Explore node types
python -m zabob_houdini info types sop
python -m zabob_houdini info categories
```

**Version Management:**
```bash
# List available versions
python -m zabob_houdini houdini versions --dev

# Download specific version
python -m zabob_houdini houdini download 21.0.512 --arch arm64

# Show build information
python -m zabob_houdini houdini show 21.0.512
```

## Exit Codes

- `0`: Success
- `1`: General error or validation failure
- Other codes may be returned by specific commands

## Troubleshooting

**Common Issues:**

1. **"Houdini environment is not available"**
   - Ensure Houdini is installed and `hython` is in PATH
   - Check `python -m zabob_houdini environment` for details

2. **Download authentication errors**
   - Set `SIDEFX_USERNAME` and `SIDEFX_PASSWORD` environment variables
   - Or use `--credentials` option with .env file

3. **Package installation issues**
   - Ensure write permissions to Houdini directories
   - Run `python -m zabob_houdini environment` to verify paths

4. **Bridge communication errors**
   - Check that `hython` executable is accessible
   - Verify Houdini installation is complete and functional

For more help, use `--help` with any command or subcommand.
