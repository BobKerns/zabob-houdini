# PyPI Publishing Setup

This document describes the GitHub Actions workflow for publishing `zabob-houdini` to PyPI.

## Workflow Overview

The publishing workflow (`.github/workflows/publish.yml`) provides:

### Automated Publishing

- **Tag-based releases**: Push a `v*.*.*` tag to trigger automatic PyPI publishing
- **Manual dispatch**: Use GitHub Actions UI to publish to TestPyPI or PyPI
- **Quality gates**: Runs tests, spell check, and package verification before publishing

### Multiple Environments

- **TestPyPI**: For testing package uploads before production
- **PyPI**: For production releases
- **GitHub Releases**: Automatic release creation with built packages

## Setup Requirements

### 1. PyPI Trusted Publishing (Recommended)

Configure trusted publishing in your PyPI project settings:

- Publisher: GitHub
- Owner: `BobKerns`
- Repository: `zabob-houdini`
- Workflow: `publish.yml`
- Environment: `pypi` (and `testpypi` for testing)

### 2. Alternative: API Tokens

If not using trusted publishing, add these repository secrets:

- `PYPI_API_TOKEN`: Production PyPI token
- `TEST_PYPI_API_TOKEN`: Test PyPI token

### 3. GitHub Environments

Create these environments in repository settings:

- `pypi` - for production publishing
- `testpypi` - for test publishing

## Usage

### Automatic Release

```bash
# Create and push a version tag
git tag v0.1.1
git push origin v0.1.1
```

This will:

1. Build and test the package
2. Publish to PyPI
3. Create a GitHub release
4. Attach build artifacts

### Manual Testing

1. Go to Actions → Publish to PyPI
2. Click "Run workflow"
3. Select "testpypi"
4. Click "Run workflow"

### Version Management

Update version in `pyproject.toml` before creating tags:

```toml
[project]
name = "zabob-houdini"
version = "0.1.1"  # Update this
```

## Package Configuration

### PyPI Metadata

- **Name**: `zabob-houdini`
- **License**: MIT
- **Keywords**: houdini, 3d, graphics, procedural, node-graph, vfx
- **Classifiers**: Appropriate for 3D/VFX Python libraries

### Build System

- **Backend**: hatchling (modern Python packaging)
- **Dependencies**: Listed in `pyproject.toml`
- **Scripts**: `zabob-houdini` CLI entry point

## Verification

After publishing, verify the package:

```bash
# Install from PyPI
pip install zabob-houdini

# Test CLI
zabob-houdini --version

# Test import
python -c "from zabob_houdini import node, chain; print('Import successful')"
```

## Troubleshooting

### Common Issues

1. **Package name conflicts**: Ensure `zabob-houdini` is available on PyPI
2. **Permission errors**: Check trusted publishing or token configuration
3. **Build failures**: Review test output and package structure
4. **Upload failures**: Verify environment configuration and secrets

### Debugging

- Check workflow logs in GitHub Actions
- Test locally with `uv build`
- Verify package contents in `dist/` directory

## Security

- Uses OpenID Connect (OIDC) for trusted publishing
- No long-lived secrets stored in repository
- Environment protection rules prevent unauthorized publishing
- All uploads are cryptographically signed
