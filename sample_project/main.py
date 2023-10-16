from wepps import Site
import sys


if __name__ == "__main__":
    dev_mode = len(sys.argv) > 1 and sys.argv[1] == "--dev"
    site = Site(
        apps_path="web_apps",
        enforce_dev_mode=dev_mode,
        escape_html_in_md=False,
        verbose=dev_mode,
    )
    site.run()
