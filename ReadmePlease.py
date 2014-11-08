import sublime
import sublime_plugin

import sys

# On Windows and OSX, with (commonly) case-insensitive file systems,
# don't bother trying different upper-/lower-case spellings
if sys.platform in ('win32', 'darwin'):
    README_PATTERNS = ['readme.*']
else:
    README_PATTERNS = ["readme.*", "README.*", "Readme.*", "ReadMe.*"]


class ReadmePleaseCommand(sublime_plugin.WindowCommand):

    def description(self):
        """Quick access to packages README."""

    def run(self):

        self.helps = []

        for spelling in README_PATTERNS:
            for path in sublime.find_resources(spelling):
                components = path.split('/')
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
