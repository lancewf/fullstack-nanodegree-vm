from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from restaurant_data import restaurantQuery
app = Flask(__name__)

@app.route('/')
@app.route('/restaurants')
def restaurants():
	with restaurantQuery() as query:
		restaurants = query.getAllRestaurants()

	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		name = request.form['name']
		with restaurantQuery() as query:
			query.createNewRestaurant(name)
		flash("new restaurant created!")
		return redirect(url_for('restaurants'))
	else:
		return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
	with restaurantQuery() as query:
		restaurant = query.getRestaurantFromId(restaurant_id)
		menuItems = query.getRestaurantMenuItems(restaurant.id)

	return render_template('menu.html', restaurant=restaurant, items=menuItems)

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	if request.method == 'POST':
		updatedName = request.form['name']
		with restaurantQuery() as query:
			query.renameRestaurant(restaurant_id, updatedName)
		flash("restaurant edit!")
		return redirect(url_for('restaurants'))
	else:
		with restaurantQuery() as query:
			restaurant = query.getRestaurantFromId(restaurant_id)

		return render_template('editrestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	if request.method == 'POST':
		with restaurantQuery() as query:
			query.deleteRestaurant(restaurant_id)
		flash("restaurant deleted!")
		return redirect(url_for('restaurants'))
	else:
		with restaurantQuery() as query:
			restaurant = query.getRestaurantFromId(restaurant_id)
		return render_template('deleterestaurant.html', restaurant=restaurant)


# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		menuItemName = request.form['name']
		with restaurantQuery() as query:
			query.createNewMenuItem(menuItemName, restaurant_id)
		flash("new menu item created!")
		return redirect(url_for('restaurantMenu', restaurant_id= restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id= restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	if request.method == 'POST':
		updatedMenuItemName = request.form['name']
		with restaurantQuery() as query:
			query.renameMenuItem(menu_id, updatedMenuItemName)
		flash("menu item edit!")
		return redirect(url_for('restaurantMenu', restaurant_id= restaurant_id))
	else:
		with restaurantQuery() as query:
			item = query.getMenuItemFromId(menu_id)
		return render_template('editmenuitem.html', restaurant_id= restaurant_id, item=item)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	if request.method == 'POST':
		with restaurantQuery() as query:
			query.deleteMenuItem(menu_id)
		flash("menu item deleted!")
		return redirect(url_for('restaurantMenu', restaurant_id= restaurant_id))
	else:
		with restaurantQuery() as query:
			item = query.getMenuItemFromId(menu_id)
		return render_template('deletemenuitem.html', item=item)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	with restaurantQuery() as query:
		restaurant = query.getRestaurantFromId(restaurant_id)
		menuItems = query.getRestaurantMenuItems(restaurant.id)

	return jsonify(MenuItems=[i.serialize for i in menuItems])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	with restaurantQuery() as query:
		menuItem = query.getMenuItemFromId(menu_id)

	return jsonify(MenuItem=menuItem.serialize)


if __name__ == '__main__':
	app.secret_key = "super_secret_key"
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)