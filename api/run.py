from main import create_app
import os
# import logging




if __name__ == "__main__":
  app = create_app()
  PORT = int(os.environ.get('PORT', app.config["FLASK_PORT"]))
  app.run(debug=True,host=app.config["FLASK_DOMAIN"], port=app.config["FLASK_PORT"])
# else:
#   app = create_app()
#   logging.basicConfig(app.config["FLASK_DIRECTORY"] + "trace.log", level=logging.DEBUG)