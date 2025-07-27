"""__init__.py for music_piece package"""

import warnings

# Suppress deprecation warnings from pkg_resources imported from pretty_midi
warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API")
