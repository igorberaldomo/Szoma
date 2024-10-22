def find_rgb(uploaded_image):
    ct = ColorThief(uploaded_image)
    cor = ct.get_color(quality=1)
    print(cor)