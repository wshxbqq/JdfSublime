import sublime, sublime_plugin
import os
import subprocess

isBusy=False;

class JdfSublimeCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		global isBusy
		isBusy=True;
		path=self.view.file_name()

		p_array=path.split("\\")
		pathCfg= self.getPathContainsCfg(path)
		bat_path=os.getcwd()+"\\jdf_start.bat"
		proce = subprocess.Popen([bat_path,pathCfg,path,p_array[0]],shell=True,stdout=subprocess.PIPE)
		output=proce.communicate()
		isBusy=False;
		sublime.message_dialog("submit ok!")


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

class JdfSublimeUploadFolderCommand(sublime_plugin.WindowCommand):
	def run(self, paths):
		global isBusy
		isBusy=True;
		path= paths[0]
		p_array=path.split("\\")
		pathCfg= self.getPathContainsCfg(path)
		bat_path=os.getcwd()+"\\jdf_start.bat"
		proce = subprocess.Popen([bat_path,pathCfg,path,p_array[0]],shell=True,stdout=subprocess.PIPE)
		output=proce.communicate()
		isBusy=False;
		sublime.message_dialog("submit ok!")

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
