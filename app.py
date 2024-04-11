from app import create_app


if __name__ == "__main__":
    app, db = create_app()
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
