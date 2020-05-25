from flask_table import Table, Col, LinkCol
from flask import Flask, Markup, request, url_for
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)


class SortableTable(Table):
    id = Col('ID')
    name = Col('Country Name')
    continent = Col('Continent')
    year = Col('Year')
    lifeExp = Col('Life exp')
    pop = Col('Population')
    gdpPercap = Col('GDP per Cap')
    link = LinkCol(
        'Link', 'flask_link', url_kwargs=dict(name='name'), allow_sort=False)
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_key, direction=direction)


@app.route('/')
def index():
    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = SortableTable(Item.get_sorted_by(sort, reverse),
                          sort_by=sort,
                          sort_reverse=reverse)
    return table.__html__()


@app.route('/item/<string:name>')
def flask_link(name):
    df = px.data.gapminder()
    fig = px.scatter(df.query('country=="{}"'.format(name)), x="year", y="gdpPercap",
                     size="pop", color="lifeExp",
                     hover_name="country", log_x=True, size_max=60)

    return fig.to_html(full_html=False)


class Item(object):
    def __init__(self, id, name, continent, year, lifeExp, pop, gdpPercap):
        self.id = id
        self.name = name
        self.continent = continent
        self.year = year
        self.lifeExp = lifeExp
        self.pop = pop
        self.gdpPercap = gdpPercap

    @classmethod
    def get_elements(cls):
        elements = []
        current_id = 0
        df = px.data.gapminder()

        for country in df['country']:
            elements.append(
                Item(current_id, country, df.continent[current_id],
                     df.year[current_id], round(df.lifeExp[current_id], 1), df['pop'][current_id], round(df.gdpPercap[current_id], 1)))
            current_id = current_id + 1

        return elements

    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        return sorted(
            cls.get_elements(),
            key=lambda x: getattr(x, sort),
            reverse=reverse)

    @classmethod
    def get_element_by_id(cls, id):
        return [i for i in cls.get_elements() if i.id == id][0]


if __name__ == '__main__':
    app.run(debug=True)
