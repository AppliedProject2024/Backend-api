from routes.init import create_app

#run app
app = create_app()

#if script is run directly
if __name__ == '__main__':
    app.run(debug=True)