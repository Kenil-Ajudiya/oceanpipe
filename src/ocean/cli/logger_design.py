import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme


def setup_logger(log_level: int = logging.INFO, log_file: str = "ocean.log"):
    """Configures the root logger for both console (Rich) and file output."""

    # 1. Set up the File Handler
    # We use a standard formatter here so the file is clean, searchable text.
    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    # 2. Set up the Console Handler with custom styles
    # Define custom theme for logger styles
    custom_theme = Theme(
        {
            "logging.level.debug": "bold cyan",
            "logging.level.info": "bold green",
            "logging.level.warning": "bold yellow",
            "logging.level.error": "bold red",
            "logging.level.critical": "bold red",
            "log.time": "bold blue",
        }
    )
    # Create a Rich Console with the custom theme
    rich_console = Console(theme=custom_theme, stderr=True)

    # RichHandler automatically adds color, timestamps, and beautiful tracebacks.
    console_handler = RichHandler(
        console=rich_console,
        rich_tracebacks=True,
        markup=True,
        show_time=True,
        log_time_format="[%Y-%m-%d %H:%M:%S]",
    )

    # 3. Configure the Root Logger
    # By passing both handlers to basicConfig, all modules will output to both!
    logging.basicConfig(
        level=log_level,
        format="%(message)s",  # RichHandler uses this minimal format
        handlers=[console_handler, file_handler],
    )
