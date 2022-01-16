from os import path
import markdown
import datetime
import pathlib
import config
import packaging.version
class PageConfigNotFound(Exception):pass
class page:
    def __init__(self,text:str):
        self.config=config.load()
        if isinstance(self.config.get("version"),str):
            self.version=packaging.version.parse(self.config["version"])
        else:
            self.version=packaging.version.parse("1.0.0")
        self.md=markdown.Markdown(
            extensions=[
                "extra",
                "admonition",
                "codehilite",
                "legacy_attrs",
                "legacy_em",
                "nl2br",
                "sane_lists",
                "toc",
                "wikilinks",
                "meta",
                "smarty"
            ],
            extension_configs={
                "toc":{
                    "title": "目次"
                },
                "codehilite":{
                    "pygments_style": "solarized-dark",
                    "noclasses": True
                }
            }
        )
        self.text=self.md.convert(text)
        self.meta=self.md.Meta
        self.type=self.meta.get("type")[0]
        self.pagesetting=config.pageconf(self.config["pagesettings"].get(self.type),self.config).themeconf
        self.temprateroot=pathlib.Path(self.config["builderpath"])/self.config["temprateroot"]
        self.title=self.meta["title"][0]
        self.dateformat=self.meta.get("dateformat") if isinstance(self.meta.get("dateformat"),str) else (self.pagesetting["replacer"].get("date_format") if isinstance(self.pagesetting["replacer"].get("date_format"),str) else "%m-%d-%Y %H:%M")
        self.date=datetime.datetime.strptime(self.meta["date"][0],"%m-%d-%Y %H:%M").strftime(self.dateformat)
        self.updatedate=self.meta.get("updatedate")
        if self.updatedate is list:
            self.updatedate=self.updatedate[0]
            self.updatedate=datetime.datetime.strptime(self.updatedate,"%m-%d-%Y %H:%M").strftime(self.dateformat)
        else:self.updatedate="NO-DATE"
        self.summary=self.meta.get("summary")
        if self.summary is list:self.summary[0]
        
        
    def build(self) -> str:
        text=""
        with open(pathlib.Path(self.pagesetting["root"])/self.pagesetting["file"],"r",encoding="utf_8")as f:text=f.read()
        replacer=self.pagesetting["replacer"]
        for n,f in self.pagesetting["pageplace"].items():
            data=""
            with open(pathlib.Path(self.pagesetting["root"])/f,"r",encoding="utf-8")as file:data=file.read()
            text=text.replace(f"<+!+ {n} +!+>",data)
        text=text.replace(replacer["text"],self.text)
        text=text.replace(replacer["date"],self.date)
        text=text.replace(replacer["title"],self.title)
        text=text.replace(replacer["update-date"],str(self.updatedate))
        return text
