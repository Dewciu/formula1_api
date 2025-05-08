from formula1_app import get_app
import matplotlib

matplotlib.use("SVG")
if __name__ == "__main__":
    print("Starting the app...")
    app = get_app()
    app.run(debug=True)
