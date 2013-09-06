import sublime, sublime_plugin, subprocess, os, signal

class AromaHelper:
  
  @staticmethod
  def settings(key):
    if not hasattr(AromaHelper, '_settings'):
      AromaHelper._settings = sublime.load_settings('Aroma.sublime-settings')

    return AromaHelper._settings.get(key)

#------

class AromaCompiler:
  _watching = {}
  @staticmethod
  def run(*opts):
    args = ["aroma"]
    for opt in opts:
      args.append(opt)
    ext = AromaHelper.settings('use_extension')
    if ext:
      args.append("-e")
      args.append(ext)
    print ("Aroma Process Args",args)
    return subprocess.Popen(args, stdout=subprocess.PIPE)

  @staticmethod
  def compile(source):
    pro = AromaCompiler.run("-c", source)
    (out, err) = pro.communicate()
    if out:
      print ("program output:", out)
    if err:
      print ("program error:", err)

  @staticmethod
  def watch(source):
    pro = AromaCompiler.run("-wc", source)
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
