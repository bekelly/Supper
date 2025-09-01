from config import load_config
from render import Renderer

def main():
    config = load_config()
    renderer = Renderer(config)

    # Show boot splash
    renderer.show_image("assets/boot.png")

    # TODO: start scheduler
    # TODO: start command listener

    # Block main thread
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nSupper shutting down gracefully.")

if __name__ == "__main__":
    main()