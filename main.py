from app import app
from models.quotes import Quote

if __name__ == "__main__":
    Quote.create_table(True)
    app.run()
