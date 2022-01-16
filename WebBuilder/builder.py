import page
import config
import pathlib
import glob
import math
import packaging.version
import warnings
import shutil
class builder:
    def __init__(self):
        self.config=config.load()
        self.filelist=glob.glob(str(pathlib.PurePath(self.config["root"])/"**"))
        if isinstance(self.config.get("version"),str):
            self.version=packaging.version.parse(self.config["version"])
        else:
            self.version=packaging.version.parse("1.0.0")
        self.version_check()
        
    def version_check(self):
        if self.version<config.version:
            warnings.warn(f"The WebBuilder's version is {config.version}. But configuration file version is {self.version}.\nThere are a lot of risks about the version that doesn't match.",RuntimeWarning)
        elif self.version>config.version:
            raise RuntimeError(f"The WebBuilder's version is {config.version}. But configuration file version is {self.version}.\nThere are a lot of risks! Please update the WebBuilder!")
        if config.version.is_devrelease:
            warnings.warn(f"This WebBuilder is in development version! There are a lot of risks to use this!",RuntimeWarning)
        if config.version.is_prerelease:
            warnings.warn(f"This WebBuilder is in pre-release version! There are some risks to use this!",RuntimeWarning)
    def __format_progress(self,tasks,complated):
        text="\033[42m"
        text+=" "*(math.floor((shutil.get_terminal_size()[0]-4)*(complated/tasks)))
        text+="\033[47m"
        text+=" "*(math.floor((shutil.get_terminal_size()[0]-4)*(1-(complated/tasks))))
        text+="\033[46m\033[31m"
        text+="{:<3d}%".format(int(complated/tasks))
        text+="\033[0m"
        return text
    def __output(self,string,end="\n"):
        text=string
        if len(string)<shutil.get_terminal_size()[0]:
            string+=" "*(shutil.get_terminal_size()[0]-len(string))
        print(string,end=end)
    def build(self,output=False):
        all_tasks=len(self.filelist)
        complated_tasks=-1
        for f in self.filelist:
            complated_tasks+=1
            is_match=False
            if output:self.__output(self.__format_progress(all_tasks,complated_tasks),end="\r")
            if pathlib.Path(f).is_dir():continue
            for p in self.config["disable-pattern"]:
                if pathlib.Path(f).match(p):is_match=True
            if is_match:continue
            if pathlib.Path(f).match("*.md"):
                with open(f,"tr")as file:data=file.read()
                data=page.page(data).build()
                if output:self.__output(f"Building file... {f}")
                if output:self.__output(self.__format_progress(all_tasks,complated_tasks),end="\r")
                with open(((pathlib.Path(self.config["built-data-root-path"])/(pathlib.Path(self.config["root"])/pathlib.Path(f).relative_to("./root")).relative_to("./root")).resolve().with_suffix(".html")),"w")as file:file.write(data)
            else:
                if output:self.__output(f"Copying file... {f}")
                if output:self.__output(self.__format_progress(all_tasks,complated_tasks),end="\r")
                with open(f,"br")as file:data=file.read()
                with open((pathlib.Path(self.config["built-data-root-path"])/(pathlib.Path(self.config["root"])/pathlib.Path(f).relative_to("./root")).relative_to("./root")).resolve(),"bw")as file:file.write(data)
            if output:self.__output(self.__format_progress(all_tasks,complated_tasks),end="\r")
        if output:print()
if __name__=="__main__":
    builder().build(output=True)