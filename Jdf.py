import sublime, sublime_plugin
import os
import subprocess
import thread

class JdfSublimeBaseCommand(sublime_plugin.WindowCommand):
	def panel(self, output, clear=True, **kwargs):
		if not hasattr(self, 'output_view'):
			self.output_view = self.window.get_output_panel("git")
		self.output_view.set_read_only(False)
		self._output_to_view(self.output_view, output, clear=clear, **kwargs)
		self.output_view.set_read_only(True)
		self.window.run_command("show_panel", {"panel": "output.git"})

	def _output_to_view(self, output_file, output, clear=False):
		output_file.set_syntax_file("Packages/JavaScript/JavaScript.tmLanguage")
		edit = output_file.begin_edit()
		if clear:
			region = sublime.Region(0, self.output_view.size())
			output_file.erase(edit, region)
		output_file.insert(edit, self.output_view.size(), output)
		output_file.end_edit(edit)


	def startThread(self,args):
		winCmdStr=self.winDisk+" &cd "+self.pathCfg+"& jdf upload "+self.shortPath
		if args:
			winCmdStr+=" -debug"
		proce = subprocess.Popen(winCmdStr,shell=True,stdout=subprocess.PIPE)
		self.output=proce.communicate()[0]
		self.isReady=True
		print winCmdStr

	def cb(self):
		if self.isReady is not True:
			sublime.set_timeout(self.cb,100)
			pass
		else:
			self.panel("\n"+self.output,False)


	def getPathContainsCfg(self, path):
		exists=False;
		p_array=path.split("\\")
		exists = os.path.exists("\\".join(p_array)+"\\config.json")
		while exists is not True :
			if len(p_array)<=1:
				return False
				pass
			p_array.pop()
			exists = os.path.exists("\\".join(p_array)+"\\config.json")
			pass
		return "\\".join(p_array)
		return exists

class JdfSublimeShortCutBase(JdfSublimeBaseCommand):
	def initArgs(self,isDebug):
		self.output=None
		self.isReady=False
		self.path=self.window.active_view().file_name()
		self.pathCfg= self.getPathContainsCfg(self.path)
		self.winDisk=self.path.split("\\")[0]
		if self.pathCfg is False:
			sublime.message_dialog("This folder or parents are not contains config.json!")
			return
			pass
		self.shortPath=self.path.replace(self.pathCfg+"\\","");
		initStr="Exec Command: jdf upload "+self.shortPath+"";
		if isDebug:
			initStr+=" -debug"
			pass
		self.panel(initStr+"\nPlease Wait....\n----------------------------------------------")
		thread.start_new_thread(self.startThread,(isDebug,)) 
		sublime.set_timeout(self.cb,100)
		pass



class JdfSublimeCompressedCommand(JdfSublimeShortCutBase):
	def run(self):
		self.initArgs(False)
		pass

		

class JdfSublimeDebugerCommand(JdfSublimeShortCutBase):
	def run(self):
		self.initArgs(True)
		pass


class JdfSublimeUploadFolderBase(JdfSublimeBaseCommand):
	def initArgs(self,path,isdebug):
		self.output=None
		self.isReady=False
		self.path=path
		self.pathCfg= self.getPathContainsCfg(self.path)
		self.winDisk=self.path.split("\\")[0]
		if self.pathCfg is False:
			sublime.message_dialog("This folder or parents are not contains config.json!")
			return
			pass
		if self.path == self.pathCfg:
			self.shortPath=""
			pass
		else:
			self.shortPath=self.path.replace(self.pathCfg+"\\","");
		initStr="Exec Command: jdf upload "+self.shortPath+"";
		if isdebug:
			initStr+=" -debug"
			pass
		self.panel(initStr+"\nPlease Wait....\n----------------------------------------------")
		thread.start_new_thread(self.startThread,(isdebug,)) 
		sublime.set_timeout(self.cb,100)
		pass


class JdfSublimeUploadFolderCompressedCommand(JdfSublimeUploadFolderBase):
	def run(self, paths):
		self.path=paths[0]
		self.initArgs(self.path,False);

class JdfSublimeUploadFolderDebugCommand(JdfSublimeUploadFolderBase):
	def run(self, paths):
		self.path=paths[0]
		self.initArgs(self.path,True);