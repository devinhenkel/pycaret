"""
Main entry point for PyCaret ML Workflow Manager application.
"""

from src.app import create_app


def main():
    """Launch the Gradio application."""
    app = create_app()
    app.launch(share=False, server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
