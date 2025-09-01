from pathlib import Path
from config import load_config
from render import Renderer
from artwork import get_artwork

def main():
    config = load_config()
    renderer = Renderer(config)

    # Show boot splash
    renderer.show_image("assets/boot.png")

    # TODO: start scheduler
    # TODO: start command listener

    try:
        art_path = get_artwork("Danielle Ate the Sandwich", "Fumbling")
    except Exception:
        art_path = Path("assets/fallback.png")

    renderer.show_image(str(art_path))

    # Block main thread
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nSupper shutting down gracefully.")

if __name__ == "__main__":
    main()