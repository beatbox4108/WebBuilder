import yaml
import pathlib
import packaging.version

def load() -> dict:
    with open("./pagebuild.yaml","r",encoding="utf-8")as f:config=yaml.safe_load(f)
    return config

class pageconf:
    def __init__(self,code:dict,conf:dict):
        self.config=conf
        self.code=code
        self.themeconf:dict={}
        if code.get("theme"):
            path=pathlib.Path(self.config["builderpath"])/self.config["themeroot"]/self.code["theme"]/"theme.yaml"
            with open(path,"r",encoding="utf_8")as f:
                self.themeconf=yaml.safe_load(f)
            if not isinstance(self.themeconf.get("root"),str):
                self.themeconf["root"]=str(pathlib.Path(self.config["builderpath"])/self.config["themeroot"]/self.code["theme"])
            else:
                self.themeconf["root"]=str(pathlib.Path(self.config["builderpath"])/self.config["themeroot"]/self.code["theme"]/self.themeconf["root"])
        else:
            self.themeconf=code
            if not isinstance(self.themeconf.get("root"),str):
                self.themeconf["root"]=str(pathlib.Path(self.config["builderpath"])/self.config["temprateroot"])
version=packaging.version.parse("1.0.1")
            
        
