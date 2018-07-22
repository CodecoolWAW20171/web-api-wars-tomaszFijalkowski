from configparser import ConfigParser


def config(filename='settings.ini', section="postgres"):
    parser = ConfigParser()
    parser.read(filename)

    data = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            data[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))
            
    return data


def sqlalchemy_connection(filename='settings.ini', section="flask"):
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        return parser.get(section, 'sqlalchemy_connection')
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))


def secret_key(filename='settings.ini', section="flask"):
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        return parser.get(section, 'secret_key')
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))
