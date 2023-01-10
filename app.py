from components import create_app


app = create_app()

app.run(
    host = "0.0.0.0",
    port=16346,
    debug=True
)