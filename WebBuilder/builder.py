import page
import config
import pathlib
import glob
import re
import packaging.version
import warnings
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

    def build(self):
        for f in self.filelist:
            is_match=False
            if pathlib.Path(f).is_dir():continue
            for p in self.config["disable-pattern"]:
                if pathlib.Path(f).match(p):is_match=True
            if is_match:continue
            if pathlib.Path(f).match("*.md"):
                with open(f,"tr")as file:data=file.read()
                data=page.page(data).build()
                with open(((pathlib.Path(self.config["built-data-root-path"])/(pathlib.Path(self.config["root"])/pathlib.Path(f).relative_to("./root")).relative_to("./root")).resolve().with_suffix(".html")),"w")as file:file.write(data)
            else:
                with open(f,"br")as file:data=file.read()
                with open((pathlib.Path(self.config["built-data-root-path"])/(pathlib.Path(self.config["root"])/pathlib.Path(f).relative_to("./root")).relative_to("./root")).resolve(),"bw")as file:file.write(data)
                
if __name__=="__main__":
    builder().build()