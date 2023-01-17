from chars.tables import ByteTables

from ..util.jinja2 import get_template


def generate(wcwidth9_tables: ByteTables):
    template = get_template('lookup.rs.j2')
    print(template.render(tables=wcwidth9_tables).strip())
