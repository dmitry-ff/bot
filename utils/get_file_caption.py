def get_file_caption(event):
    return event.data["parts"][0]["payload"]["caption"]