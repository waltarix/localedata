from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))


def get_template(name: str):
    return env.get_template(name)
