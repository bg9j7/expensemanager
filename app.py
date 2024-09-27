from app import create_app

"""
    Initializes the Flask application and runs it.

    This function creates an instance of the Flask application using the `create_app` function
    from the `app` module. It then runs the application using the `run` method of the Flask
    application instance.

    Returns:
        app: An instance of the Flask application.
    """
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)