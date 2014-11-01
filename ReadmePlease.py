import sublime
import sublime_plugin

import os
import sys

# On Windows and OSX, with (commonly) case-insensitive file systems,
# don't bother trying different upper-/lower-case spellings
if sys.platform in ('win32', 'darwin'):
    README_PATTERNS = ['readme.*']
else:
    README_PATTERNS = ["readme.*", "README.*", "Readme.*", "ReadMe.*"]


try:
    find_resources = sublime.find_resources
except AttributeError:
    import glob
    def find_resources(pattern):
        """ Fallback for ST2, where sublime.find_resources does not exist;
            unlike the original, this function does only perform a NON-RECURSIVE
            lookup inside sublime.packages_path(), which is all that's needed.
        """
        packages_path = sublime.packages_path()
        base_path = os.path.dirname(packages_path)
        path_pattern = os.path.join(packages_path, '*', pattern)
        paths = glob.glob(path_pattern)
        return (os.path.relpath(p, start=base_path) for p in paths)


class ReadmePleaseCommand(sublime_plugin.WindowCommand):

    def description(self):
        """Quick access to packages README."""

    def run(self):

        self.helps = []

        for spelling in README_PATTERNS:
            for path in find_resources(spelling):
                components = path.split(os.path.sep)
                if len(components) == 3:      # exclude files in package subdirs
                    package_name, readme_name = components[-2:]
                    self.helps.append([package_name, readme_name, path])

        self.helps.sort()
        self.window.show_quick_panel(list(map(
            lambda x: [x[0], x[1]], self.helps)), self.onSelect)

    def onSelect(self, i):
        if (i != -1):
            help = self.helps[i]

            sublime.active_window().run_command("open_file", {
                "file": "${packages}/%s/%s" % (help[0], help[1])})
