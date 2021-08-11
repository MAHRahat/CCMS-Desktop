# Password lengths
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 20
# Server URL (with port)
SERVER_URL = "http://127.0.0.1:8080"  # FixMe: SERVER_URL needs to be changed
# REST API Endpoints
EP_REGISTER = "/rest-auth/registration/"
EP_LOGIN = "/rest-auth/login/"
EP_LOGOUT = "/rest-auth/logout/"
EP_USER = "/rest-auth/user/"
EP_PASSWORD_CHANGE = "/rest-auth/password/change/"
EP_PASSWORD_RESET = None
EP_USERS = "/users"
EP_CITIZENS = "/citizens"
EP_EMPLOYEES = "/employees"
EP_UPDATE_PROFILE = "/users/"  # Need to append id
EP_CATEGORIES = "/categories"  # GET, POST, DELETE
EP_CATEGORY = "/categories/"  # Need to append id  # GET, PUT/PATCH, DELETE
EP_COMPLAINTS = "/complaints"
EP_COMPLAINTS_BY_USER = "/complaints/user/"  # Need to append id
