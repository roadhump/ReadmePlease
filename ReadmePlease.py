import sublime, sublime_plugin
import os
import re

class ReadmePleaseCommand(sublime_plugin.WindowCommand):

    def description(self):
        'Quick access to packages README'

    def run(self):
        package_names = os.listdir(sublime.packages_path())

        self.helps = []

        for path in package_names:
            package_path = os.path.join(sublime.packages_path(), path)
            if (os.path.isdir(package_path)):
                fs = [file for file in os.listdir(package_path) if re.match('readme', file, flags=re.IGNORECASE)]
                if len(fs):
                    self.helps.append([path, fs[0], os.path.join(package_path, fs[0])])

        self.helps.sort()
        self.window.show_quick_panel(map(lambda x: [x[0], x[1]], self.helps), self.onSelect)

    def onSelect(self, i):
        if (i != -1):
            help = self.helps[i]
            help_view = self.window.open_file(help[2])
            help_view.set_read_only(True)
