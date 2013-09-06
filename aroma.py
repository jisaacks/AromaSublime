import sublime, sublime_plugin, subprocess, os, signal

class AromaCompiler:
  _watching = {}

  @staticmethod
  def compile(source):
    pro = subprocess.Popen(["aroma", "-c", source], stdout=subprocess.PIPE)
    (out, err) = pro.communicate()
    if out:
      print ("program output:", out)
    if err:
      print ("program error:", err)

  @staticmethod
  def watch(source):
    pro = subprocess.Popen(["aroma", "-wc", source, "&"], stdout=subprocess.PIPE)
    print ("Aroma Watching:",source)
    AromaCompiler._watching[source] = pro.pid

  @staticmethod
  def unwatch(source):
    print ("Aroma Unwatching:",source)
    pid = AromaCompiler._watching[source]
    print ("Aroma attempting to kill:",pid)
    os.kill(pid, signal.SIGTERM)

#------

class AromaCompileAllCommand(sublime_plugin.WindowCommand):
  def run(self):
    w = self.window
    for fol in w.folders():
      AromaCompiler.compile(fol)

class AromaCompileCurrentCommand(sublime_plugin.WindowCommand):
  def run(self):
    v = self.window.active_view()
    fil = v.file_name()
    AromaCompiler.compile(fil)

class AromaWatchCurrentCommand(sublime_plugin.WindowCommand):
  def run(self):
    v = self.window.active_view()
    fil = v.file_name()
    AromaCompiler.watch(fil)

class AromaUnwatchCurrentCommand(sublime_plugin.WindowCommand):
  def run(self):
    v = self.window.active_view()
    fil = v.file_name()
    AromaCompiler.unwatch(fil)
