from configparser import ConfigParser

def load_config(filename='db.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        for k, v in parser.items(section):
            config[k] = v
    else:
        raise Exception(f'Section {section} not found in {filename}')
    return config
