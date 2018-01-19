import os
from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter, get_page_args
from model import *


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


app = Flask(__name__)
db = SQLAlchemy(app)

# config
app.config.from_object('config.BaseConfig')
env = 'DEV'
conf = {
    'DEV': 'config.DevelopmentConfig',
    'PROD': 'config.CloudConfig'
}
os.environ['APP_SETTINGS'] = conf[env]
app.config.from_object(os.environ['APP_SETTINGS'])
user_table_name = app.config.get('ARTICLE_TABLE_NAME')
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
def home(page):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    # all_articles = db.session.query(RelatedArticles).all()
    articles = db.session.query(RelatedArticles).order_by(RelatedArticles.related_probability).limit(per_page).offset(offset)
    count = db.session.query(RelatedArticles).count()
    if not articles and page != 1:
        abort(404)
    pagination = Pagination(page, per_page, count)
    return render_template('index.html', pagination=pagination, articles=articles)


if __name__ == '__main__':
    app.run(debug=False)
