import pagebuilder.page
import pagebuilder.config
import glob

conf=pagebuilder.config.load()
glob.glob(conf["root"])