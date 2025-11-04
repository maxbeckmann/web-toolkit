"""
Compatibility launcher that delegates to the packaged example.

Running ``python main.py`` mirrors invoking ``python -m webtoolkit`` or the
``webtoolkit-example`` console script once the project is installed.
"""

from webtoolkit.example import main as example_main


def main():
    example_main()


if __name__ == "__main__":
    main()
