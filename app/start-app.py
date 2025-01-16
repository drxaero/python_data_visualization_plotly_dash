from app1 import app1

if __name__ == "__main__":
    app1.run_server(
        port=8091, debug=True
    )  # 可以指定 `host="0.0.0.0"` 或 `port=8051` 或 `debug=True` 或 `height=800` 或 `width="80%"`
