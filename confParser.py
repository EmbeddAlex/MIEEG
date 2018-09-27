from configparser import ConfigParser


class ConfParser:
    def __init__(self, val_path):
        self.conf = ConfigParser()
        self.file_path = val_path

    def read(self, section, field):
        self.conf.read(self.file_path)
        return self.conf.get(section, field)

    def write(self, section, field, value):
        self.conf.set(section, field, value)
        with open(self.file_path, "w") as config:
            self.conf.write(config)
        
    def addSection(self, sectionName):
        if not self.conf.has_section(sectionName):
            self.conf.add_section(sectionName)
        self.conf.write(open(self.file_path, "w"))


config_file = ConfParser("src/settings.conf")
