from flask import Flask 
app = Flask(__name__) 				# Create app object as FLASK (variable app)

from app import routes				# app from app package
									# import at bottom to avoid circular imports
