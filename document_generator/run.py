from os import getcwd, listdir
from pathlib import Path
from streamlit.web import cli
from sys import argv, exit
from typing import NoReturn


def run_streamlit() -> NoReturn:
    curent_directory: Path = Path(__file__).parent
    streamlit_app: Path = curent_directory / "app" / "webapp.py"
    if streamlit_app.exists:
        print(f"Found webapp at: {str(streamlit_app)}")
        argv.clear()
        argv.extend(
            [
                "streamlit",
                "run",
                str(streamlit_app),
                "--server.port=8501",
                "--server.address=127.0.0.1",
            ]
        )
        exit(cli.main())
    else:
        print(f"Error: Could not find webapp.py at {streamlit_app}")
        print("Current directory:", getcwd())
        print("Contents of directory:", listdir(curent_directory))
        exit(1)


if __name__ == "__main__":
    run_streamlit()
