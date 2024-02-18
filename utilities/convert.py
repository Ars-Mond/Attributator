from PIL import Image

def convert_png_to_ico(png_file, ico_file):
    # Open the PNG image
    png_img = Image.open(png_file)

    # Save as ICO
    png_img.save(ico_file)


if __name__ == '__main__':
    # Example usage:
    convert_png_to_ico("icon.png", "icon.ico")