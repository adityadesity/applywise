from app.db.session import engine


def test_connection():
    try:
        connection = engine.connect()
        print("Database connected successfully!")
        connection.close()
    except Exception as e:
        print("Database connection failed:", e)


test_connection()