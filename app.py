from flask import Flask, render_template, request, redirect
from database import db_session, init_db
from models.restaurants import Restaurants
import datetime
from random import choice

app = Flask(__name__)


@app.before_first_request
def init():
    init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# http://flask.pocoo.org/docs/1.0/patterns/sqlalchemy/
# 每次request结束后正确的关闭资料库的session

@app.route('/')
def start():
    now = datetime.datetime.now()
    # 获取系统时间 ex:2019-06-19 15:53:56.452153 然后添加过滤器
    return render_template('start.html', now=now)


@app.route('/draw')
def draw():
    restaurants = Restaurants.query.all()

    if not restaurants:
        return redirect('/create-restaurant')

    random_restaurant = choice(restaurants)

    restaurant = Restaurants.query.get(random_restaurant.id)
    restaurant.draw = restaurant.draw + 1

    db_session.commit()

    now = datetime.datetime.now()
    return render_template('draw.html', restaurant=restaurant, now=now)

@app.route('/create-restaurant', methods=['GET', 'POST'])
# 如果后面没有跟method 默认为GET
def create_restaurant():
    if request.method == 'POST':
        # 当POST的时候去获取输入
        name = request.form.get('name')
        description = request.form.get('description')
        site_url = request.form.get('site_url')

        restaurant = Restaurants(name=name, description=description, site_url=site_url)
        db_session.add(restaurant)
        db_session.commit()

        # return '{},{},{}'.format(name, description, site_url)
        # 测试创建传输数据
        return redirect('/restaurants')

    return render_template('create_restaurant.html')


# 这里的render_template需要import


@app.route('/restaurants')
def restaurant_list():
    restaurants = Restaurants.query.all()

    return render_template('restaurant.html', restaurants=restaurants)


@app.route('/edit-restaurant', methods=['GET', 'POST'])
def edit_resuaurant():
    id = request.args.get('id')
    # 这个id是从 edit_restaurant.html页面中的餐厅id中获取的
    # 先取餐厅id 再用id取其他的数据

    restaurant = Restaurants.query.filter(Restaurants.id == id).first()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        site_url = request.form.get('site_url')

        restaurant.name = name
        restaurant.description = description
        restaurant.site_url = site_url
        restaurant.modified_time = datetime.datetime.now()

        db_session.commit()
        # 上传到资料库里面

        return redirect('/restaurants')

    return render_template('edit_restaurant.html', restaurant=restaurant)
    # 如果是GET直接跳转到这个页面


@app.route('/delete_restaurant')
def delete_restaurant():
    id = request.args.get('id')

    restaurant = Restaurants.query.filter(Restaurants.id == id).first()

    if restaurant:
        db_session.delete(restaurant)
        db_session.commit()

    return redirect('/restaurants')


def mealformat(value):
    # 主页的时间 进行文字处理
    if value.hour in [4, 5, 6, 8, 9]:
        return 'Breakfast'
    elif value.hour in [10, 11, 12, 13, 14, 15]:
        return 'Lunch'
    elif value.hour in [16, 17, 18, 19, 20, 21]:
        return 'Dinner'
    else:
        return 'Supper'


app.jinja_env.filters['meal'] = mealformat

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    # 清掉cache重新reload
    app.run(debug=True)
# debug=True 是反馈测试debug的代码
# 正式上线后可删除
