import sublime, sublime_plugin, os, subprocess, _thread
import subprocess, time

class GobuildExCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		# Get filename
		f = self.view.file_name()
		if (f is None):
			sublime.error_message("No file input.")
			return
		f_list = f.split('/')

		# Get file name
		fileName = f_list[-1]

		# Get process name
		idx = fileName.rfind('.')
		processName = fileName[0:idx]

		# Kill process by name
		killCmd = "pkill {0}".format(processName)
		print(">>>#: Ready to kill process >>>")
		print(">>>#: {0}".format(killCmd))
		os.system(killCmd)

		path = f.replace(fileName, "")
		runCmd = "cd {0}\n/usr/local/go/bin/go run {1}".format(path,fileName)
		print(">>>#: {0}".format(runCmd))
		print(">>>#: Services ready to run.......")

		settings = sublime.load_settings('gobuildex.sublime-settings')
		mode = settings.get("mode", 0)
		print("Run mode:", mode)

		if mode==0:
			# run in iterm terminal
			appleScriptCmd = '''osascript -e 'tell application "iTerm" to activate' '''
			os.system(appleScriptCmd)
			# stop & wait iterm to run
			time.sleep(0.5)
			appleScriptCmd = '''osascript -e 'tell application "iTerm" to activate' -e 'tell application "System Events" to tell process "iTerm" to keystroke "{0}"' -e 'tell application "System Events" to tell process "iTerm" to key code 52' '''.format(runCmd)
			os.system(appleScriptCmd)
		elif mode==1:
			# Run on normal terminal
			appleScriptCmd = '''osascript -e 'tell application "Terminal" to activate' -e 'tell application "Terminal" to do script "{0}"' '''.format(runCmd)
			print(">>>#: applescript:", appleScriptCmd)
			os.system(appleScriptCmd)
		else:
			# Run on sublime console
			_thread.start_new_thread(self.goruncmd , (runCmd,))

	def goruncmd(self, runCmd):
		proc = subprocess.Popen(runCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		sublime.ok_cancel_dialog("Services is running, you can look log at console.", "I know")
		try:
			while True:
				ln = proc.stdout.readline()
				print(">>>#: ", ln)
				if not ln:
					break
		except Exception:
			print("ex >>>")

		proc.stdout.close()
		proc.wait()
		proc = None
