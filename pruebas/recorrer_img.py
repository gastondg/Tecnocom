h = corte.shape[0]
w = corte.shape[1]
# loop over the image, pixel by pixel
for y in range(0, h):
    for x in range(0, w):
        print(corte[y, x])