def image_crop_and_resize(filepath, size_pixels=256):
    from PIL import Image
    img = Image.open(filepath)

    width, height = img.size

    if width != height:
        offset = int(abs(height - width) / 2)
        if width > height:
            img = img.crop([offset, 0, width - offset, height])
        else:
            img = img.crop([0, offset, width, height - offset])

    img = img.resize((size_pixels, size_pixels), Image.ANTIALIAS)
    img.save(filepath)
