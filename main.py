from pathlib import Path
from config import load_config
from render import Renderer
from artwork import get_artwork
from network import start_listener

def main():
    config = load_config()
    renderer = Renderer(config)

    # Show boot splash
    renderer.show_image("assets/boot.png")

    # Start HTTP command listener in background
    import threading
    listener = threading.Thread(
        target=start_listener,
        args=(renderer,),
        daemon=True
    )
    listener.start()
    print("[main] Network listener started")

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