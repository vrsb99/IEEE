from website import config_app

app = config_app()

if __name__ == '__main__':
    app.run(debug=True)