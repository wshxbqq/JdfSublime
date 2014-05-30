import sublime, sublime_plugin
import os
import subprocess
import thread


connector=";"
if sublime.platform()=="windows":
	connector="&"
	pass




class JdfSublimeBaseCommand(sublime_plugin.WindowCommand):
	def initProperties(self,path):
		self.output=None
		self.isReady=False
		self.path=path
		self.pathCfg= self.getPathContainsCfg(self.path)
		if sublime.platform()=="windows":
			self.winDisk=self.path.split("\\")[0]+" "+connector
		else:
			self.winDisk=""
		if self.pathCfg is False:
			sublime.message_dialog("This folder or parents are not contains config.json!")
			self.shortPath=False
			return False
			pass
		else:
			self.shortPath=self.path.replace(self.pathCfg+"\\","")
			return True

		
		pass
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


	def startThread(self,cmdStr):
		print cmdStr
		proce = subprocess.Popen(cmdStr,shell=True,stdout=subprocess.PIPE)
		self.output=proce.communicate()[0]
		self.isReady=True

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
	def initArgs(self,cmdStr):
		initStr="Exec Command: "+cmdStr;
		self.panel(initStr+"\nPlease Wait....\n----------------------------------------------")
		thread.start_new_thread(self.startThread,(cmdStr,)) 
		sublime.set_timeout(self.cb,100)
		pass



class JdfSublimeCompressedCommand(JdfSublimeShortCutBase):
	def run(self):
		if self.initProperties(self.window.active_view().file_name()) is True:
			cmdStr=self.winDisk+"cd "+self.pathCfg+""+connector+" jdf upload "+self.shortPath
			self.initArgs(cmdStr);
			pass
		else:
			pass

		

class JdfSublimeDebugerCommand(JdfSublimeShortCutBase):
	def run(self):
		if self.initProperties(self.window.active_view().file_name()) is True:
			cmdStr=self.winDisk+"cd "+self.pathCfg+""+connector+" jdf upload "+self.shortPath+" -debug"
			self.initArgs(cmdStr);
			pass
		else:
			pass


class JdfSublimeUploadFolderBase(JdfSublimeBaseCommand):
	def initArgs(self,cmdStr):
		initStr="Exec Command: "+cmdStr;
		self.panel(initStr+"\nPlease Wait....\n----------------------------------------------")
		thread.start_new_thread(self.startThread,(cmdStr,)) 
		sublime.set_timeout(self.cb,100)
		pass








class JdfSublimeUploadFolderCompressedCommand(JdfSublimeUploadFolderBase):
	def run(self, paths):
		if self.initProperties(paths[0]) is True:
			cmdStr=self.winDisk+"cd "+self.pathCfg+""+connector+" jdf upload "+self.shortPath
			self.initArgs(cmdStr);
			pass
		else:
			pass

		

class JdfSublimeUploadFolderDebugCommand(JdfSublimeUploadFolderBase):
	def run(self, paths):
		if self.initProperties(paths[0]) is True:
			cmdStr=self.winDisk+"cd "+self.pathCfg+""+connector+" jdf upload "+self.shortPath+" -debug"
			self.initArgs(cmdStr);
			pass
		else:
			pass


class JdfSublimeOutputFolderCommand(JdfSublimeUploadFolderBase):
	def run(self, paths):
		if self.initProperties(paths[0]) is True:
			if self.pathCfg==self.shortPath:
				self.shortPath=""
				pass
			cmdStr=self.winDisk+"cd "+self.pathCfg+""+connector+" jdf output "+self.shortPath
			self.initArgs(cmdStr);
			pass
		else:
			pass

class JdfSublimeInstallFolderCommand(JdfSublimeUploadFolderBase):
	def run(self, paths):
		self.output=None
		self.isReady=False
		self.path=paths[0]
		self.pathCfg= self.getPathContainsCfg(self.path)


		if self.pathCfg is not False:
			sublime.message_dialog("Allready has a config.json!")
			return
			pass
		if sublime.platform()=="windows":
			self.winDisk=self.path.split("\\")[0]+" "+connector+""
		else:
			self.winDisk=""
		
		cmdStr=self.winDisk+"cd "+self.path+""+connector+" jdf install init"
		print self.winDisk
		self.initArgs(cmdStr);
