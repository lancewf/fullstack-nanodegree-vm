from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from contextlib import contextmanager

@contextmanager
def restaurantQuery():
	query = RestaurantQuery()
	try:
		yield query
	finally:
		query.close()

class RestaurantQuery():
	def __init__(self):
		engine = create_engine('sqlite:///restaurantmenu.db')
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind = engine)
		self.session = DBSession()

	def close(self):
		self.session.close()

	def getAllRestaurants(self):
		return self.session.query(Restaurant).all()

	def createNewRestaurant(self, name):
		newRestaurant = Restaurant(name = name)

		self.session.add(newRestaurant)
		self.session.commit()

		return newRestaurant

	def createNewMenuItem(self, name, restaurantId):
		newMenuItem = MenuItem(name = name, restaurant_id = restaurantId)

		self.session.add(newMenuItem)
		self.session.commit()

	def renameRestaurant(self, restaurantId, newName):
		updatedRestaurant = self.getRestaurantFromId(restaurantId)

		if updatedRestaurant != None:
			updatedRestaurant.name = newName
			self.session.add(updatedRestaurant)
			self.session.commit()

	def renameMenuItem(self, menuItemId, newName):
		updatedMenuItem = self.getMenuItemFromId(menuItemId)

		if updatedMenuItem != None:
			updatedMenuItem.name = newName
			self.session.add(updatedMenuItem)
			self.session.commit()

	def getMenuItemFromId(self, menuItemId):
		return self.session.query(MenuItem).get(menuItemId)

	def getRestaurantFromId(self, restaurantId):
		return self.session.query(Restaurant).get(restaurantId)

	def getRestaurantMenuItems(self, restaurantId):
		return self.session.query(MenuItem).filter_by(restaurant_id = restaurantId)

	def deleteRestaurant(self, restaurantId):
		restaurantToDelete = self.getRestaurantFromId(restaurantId)

		if restaurantToDelete != None:
			self.session.delete(restaurantToDelete)
			self.session.commit()

	def deleteMenuItem(self, menuItemId):
		menuItemToDelete = self.getMenuItemFromId(menuItemId)

		if menuItemToDelete != None:
			self.session.delete(menuItemToDelete)
			self.session.commit()