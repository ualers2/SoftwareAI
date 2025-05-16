
from modules.Chat.utils.encode_image_to_base64 import encode_image_to_base64

def build_image_messages(images):
    """
    Builds a list of image message payloads by encoding images to base64 data URLs.

    Parameters:
    ----------
    images (Iterable): A collection of image file-like objects with a 'filename' attribute.

    Returns:
    -------
    list of dict: Message dictionaries with 'image_url' fields ready for API consumption.
    """
    image_messages = []
    for image in images:
        try:
            ext = image.filename.split('.')[-1].lower()
            mime_type = f"image/{ext if ext != 'jpg' else 'jpeg'}"
            base64_str = encode_image_to_base64(image)
            image_messages.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_str}",
                    "detail": "high"
                }
            })
        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
    return image_messages
