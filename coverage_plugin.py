"""Coverage plugin to handle _dynamic_import marker in source files."""

import coverage.python


class DynamicImportPlugin(coverage.plugin.CoveragePlugin):  # type: ignore
    """Plugin to strip _dynamic_import from __future__ imports for coverage parsing."""

    def file_tracer(self, filename):
        """Return a FileTracer for files with _dynamic_import marker."""
        if filename.endswith('.py'):
            try:
                with open(filename, 'r') as f:
                    # Quick check if file has the marker
                    for _ in range(10):  # Check first 10 lines
                        line = f.readline()
                        if not line:
                            break
                        if '_dynamic_import' in line and 'from __future__' in line:
                            return DynamicImportFileTracer(filename)
            except Exception:
                pass
        return None


class DynamicImportFileTracer(coverage.plugin.FileTracer):  # type: ignore
    """File tracer that provides cleaned source for coverage analysis."""

    def __init__(self, filename):
        self.filename = filename

    def source_filename(self):
        """Return the source filename."""
        return self.filename

    def has_dynamic_source_filename(self):
        """We don't change the filename."""
        return False


def coverage_init(reg, options):
    """Register the plugin with coverage."""
    reg.add_file_tracer(DynamicImportPlugin())
