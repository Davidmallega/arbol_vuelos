from flask import Flask
from controllers.reservation_controller import control_de_reservas

app = Flask(__name__, template_folder='views/templates', static_folder='views/static')
app.register_blueprint(control_de_reservas)

if __name__ == '__main__':
    app.run(debug=True)
