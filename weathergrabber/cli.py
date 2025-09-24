import argparse
from .core import main

def main_cli():
    ## Get current locale, or use the default one
    parser = argparse.ArgumentParser(description="Weather forecast grabber from weather.com")
    parser.add_argument("--location", "-l", type=str, help="64-character-hex code for location obtained from weather.com")
    parser.add_argument("--lang", "-L", type=str, help="Language (pt-BR, fr-FR, etc.), If not set, uses the machine one.")
    parser.add_argument("--output", "-o", type=str, choices=['console','json','waybar'], default='console', help="Output format. console, json or waybar")
    parser.add_argument("--persist", "-p",action='store_true', default=False, help="Keep waybar open instead of exiting after execution. Does only makes sense for --output=console")
    parser.add_argument("--icons", "-i", type=str, choices=['fa','emoji'], default='emoji', help="Icon set. 'fa' for Font-Awesome, or 'emoji'")
    parser.add_argument(
        "--log",
        default="error",
        choices=["debug", "info", "warning", "error", "critical", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: ERROR)"
    )
    args = parser.parse_args()

    main(
        log_level=args.log,
        location=args.location,
        lang=args.lang,
        output=args.output,
        persist=args.persist,
        icons=args.icons
    )

if __name__ == "__main__":
    main_cli()

