from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash
from flask_sqlalchemy import SQLAlchemy
from contextlib import closing
from database import db_session
import cPickle as pickle

# configuration
DEBUG = True
SECRET_KEY = 'HJ%^GFYGABSDBUUAHSDS^THUASDU'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

if app.config['DEBUG']:
    from werkzeug import SharedDataMiddleware
    import os
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })

import views

@app.before_request
def before_request():
	if session.get('shopping_cart', None) == None:
		session['shopping_cart'] = pickle.dumps(views.ShoppingCart())

		
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.context_processor
def utility_processor():
    def format_price(amount, currency=u'$'):
        return u'{1}{0:.2f}'.format(amount, currency)
    return dict(format_price=format_price)

@app.context_processor
def utility_processor():
    def load_var(s):
        return pickle.loads(s)
    return dict(load_var=load_var)

"""
@app.route("/")
def index():
	cur = g.db.execute('select id, title from entries order by id desc')
	entries = [dict(id=row[0], title=row[1]) for row in cur.fetchall()]
	return render_template('index.html', entries=entries)
	
@app.route("/view_post/<id>")
def view_post(id):
	cur = g.db.execute('select id, post_date, title, body from entries where id = ?', [id])
	g.db.commit()
	entry = [dict(id=row[0], post_date=row[1], title=row[2], body=row[3]) for row in cur.fetchall()][0]
	return render_template('view_post.html', entry=entry)
	
@app.route("/submit_post", methods=['POST','GET'])
def submit_post():
	if request.method == 'POST':
		g.db.execute("insert into entries (post_date, title, body) values (date('now'), ?, ?)", [request.form['title'], request.form['body']])
		g.db.commit()
	else:
		return render_template('create_post.html', error=False)
	return redirect(url_for('index'))


if __name__ == "__main__":
	app.run(port=2000)
"""
