# VS Code Extension Documentation Disconnect Bug Report

## Summary
VS Code marketplace shows complete extension documentation (README.md) during discovery/installation, but the installed extension only displays minimal information, creating a significant user experience gap.

## Problem Description
When browsing extensions in the VS Code marketplace, users see comprehensive documentation including detailed examples, configuration options, and usage instructions. However, after installation, this documentation becomes inaccessible through the VS Code interface, leaving users without the information they need to actually use the extension.

## Expected Behavior
- Documentation visible in marketplace should match what's available after installation
- Users should have consistent access to extension documentation throughout the entire lifecycle
- Post-installation experience should provide the same level of detail as pre-installation

## Current Behavior
- **Marketplace**: Shows full README.md from source repository with examples, configuration details, and comprehensive documentation
- **Installed Extension**: Shows only basic package.json metadata - typically just name, version, and minimal description
- **User Impact**: Complete loss of actionable documentation after installation

## Specific Issues

### 1. User Experience Problems
- **Discovery Gap**: Rich documentation influences installation decisions, then vanishes
- **Usability Crisis**: Users cannot figure out how to use extensions they just installed
- **Support Burden**: No accessible help documentation for troubleshooting

### 2. Trust and Security Concerns
- **Identity Confusion**: Sparse post-install info makes it difficult to verify the correct extension was installed
- **Capability Verification**: Cannot cross-reference promised features with actual functionality
- **Version Confidence**: Hard to confirm installed extension matches marketplace expectations

### 3. Platform Design Issues
- **Inconsistent Information Architecture**: Different data sources for pre/post installation
- **Documentation Lottery**: Success depends on whether extension authors happen to bundle docs properly
- **Invisible UX Problem**: Creates friction without users understanding the root cause

## Real-World Impact
- Extensions with excellent documentation appear poorly documented after installation
- Users uninstall functional extensions because they can't figure out how to use them
- Repeated encounters with this issue across multiple extensions suggests systemic problem
- Particularly affects configuration-heavy extensions where examples are critical

## Proposed Solutions

### Option 1: Require Documentation in Package
- Mandate that comprehensive documentation be included in .vsix files
- Ensure post-install experience matches marketplace promises
- May increase package sizes but improves user experience

### Option 2: Marketplace Integration
- Provide direct access to marketplace documentation from installed extensions
- Link to source repository or cached marketplace content
- Maintains current package sizes while solving access problem

### Option 3: Clear Expectations
- Add warnings on marketplace about documentation availability post-install
- Encourage extension authors to bundle essential documentation
- Improve transparency about the documentation gap

## Technical Details
- **Root Cause**: Marketplace pulls README.md from source repository; installed extension only contains package.json metadata
- **Affected Extensions**: Particularly impacts tools like "Command Variable" and other configuration-dependent extensions
- **Scope**: Appears to be platform-wide issue affecting user experience across extension ecosystem

## Priority
**High** - This affects fundamental discoverability and usability of the extension system, creates trust issues, and represents a significant platform UX flaw that impacts all users and extension authors.

---
*This report documents a recurring issue that affects user confidence and extension adoption across the VS Code ecosystem.*
