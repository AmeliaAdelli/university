import numpy as np
import skimage as ski


def seam_carve(img, mode, mask=None):
    height = img.shape[0]
    width = img.shape[1]

    energy = np.zeros([height + 2, width + 2], dtype='float64')

    energy[1:height + 1, 1:width + 1]=img[:, :, 0] * 0.299 + img[:, :, 1] * 0.587 + img[:, :, 2] * 0.114
    energy[0:1, :] = energy[1:2, :]
    energy[:, 0:1] = energy[:, 1:2]
    energy[height + 1:, :] = energy[height:height + 1, :]
    energy[:, width + 1:] = energy[:, width:width + 1]

    gradient = np.sqrt(np.power(energy[2:, 1:width + 1] - energy[0:height, 1:width + 1], 2)
                       + np.power(energy[1:height + 1, 2:] - energy[1:height + 1, 0:width], 2))

    if mask is not None:
        gradient += mask * (height * width * 256)

    stitch = np.zeros([height, width])

    if mode == 'horizontal shrink':
        stitch[0:1, :] = gradient[0:1, :]

        for i in range(1, height):
            for j in range(0, width):
                min_neighbour = stitch[i - 1, j]
                if j != 0 and stitch[i - 1, j - 1] < min_neighbour:
                    min_neighbour = stitch[i - 1, j - 1]
                if j != width - 1 and stitch[i - 1, j + 1] < min_neighbour:
                    min_neighbour = stitch[i - 1, j + 1]

                stitch[i, j] = gradient[i, j] + min_neighbour

        x = height - 1
        y = np.argmin(stitch[x:, :])

        result = np.zeros([height, width - 1, 3])
        stitchMask = np.zeros([height, width])

        if mask is not None:
            new_mask = np.zeros([height, width - 1])
        else:
            new_mask = mask

        while x != 0:
            result[x:x + 1, :y, :] = img[x:x + 1, :y, :]
            result[x:x + 1, y:, :] = img[x:x + 1, y + 1:, :]

            if mask is not None:
                new_mask[x:x + 1, :y] = mask[x:x + 1, :y]
                new_mask[x:x + 1, y:] = mask[x:x + 1, y + 1:]

            stitchMask[x, y] = 1

            x -= 1

            min_neighbour = (stitch[x, y], 0)
            if y != 0 and stitch[x, y - 1] <= min_neighbour[0]:
                min_neighbour = (stitch[x, y - 1], -1)
            if y != width - 1 and stitch[x, y + 1] < min_neighbour[0]:
                min_neighbour = (stitch[x, y + 1], 1)
            y = y + min_neighbour[1]

        result[x:x + 1, :y, :] = img[x:x + 1, :y, :]
        result[x:x + 1, y:, :] = img[x:x + 1, y + 1:, :]

        if mask is not None:
            new_mask[x:x + 1, :y] = mask[x:x + 1, :y]
            new_mask[x:x + 1, y:] = mask[x:x + 1, y + 1:]

        stitchMask[x, y] = 1

        return [result, new_mask, stitchMask]

    if mode == 'vertical shrink':
        stitch[:, 0:1] = gradient[:, 0:1]

        for j in range(1, width):
            for i in range(0, height):
                min_neighbour = stitch[i, j - 1]
                if i != 0 and stitch[i - 1, j - 1] < min_neighbour:
                    min_neighbour = stitch[i - 1, j - 1]
                if i != height - 1 and stitch[i + 1, j - 1] < min_neighbour:
                    min_neighbour = stitch[i + 1, j - 1]
                stitch[i, j] = gradient[i, j] + min_neighbour

        y = width - 1
        x = np.argmin(stitch[:, y:])

        result = np.zeros([height - 1, width, 3])
        stitchMask = np.zeros([height, width])

        if mask is not None:
            new_mask = np.zeros([height - 1, width])
        else:
            new_mask = mask

        while y != 0:
            result[:x, y:y + 1, :] = img[:x, y:y + 1, :]
            result[x:, y:y + 1, :] = img[x + 1:, y:y + 1, :]

            if mask is not None:
                new_mask[:x, y:y + 1] = mask[:x, y:y + 1]
                new_mask[x:, y:y + 1] = mask[x + 1:, y:y + 1]

            stitchMask[x, y] = 1

            y -= 1

            min_neighbour = (stitch[x, y], 0)
            if x != 0 and stitch[x - 1, y] <= min_neighbour[0]:
                min_neighbour = (stitch[x - 1, y], -1)
            if x != height - 1 and stitch[x + 1, y] < min_neighbour[0]:
                min_neighbour = (stitch[x + 1, y], 1)
            x = x + min_neighbour[1]

        result[:x, y:y + 1, :] = img[:x, y:y + 1, :]
        result[x:, y:y + 1, :] = img[x + 1:, y:y + 1, :]

        if mask is not None:
            new_mask[:x, y:y + 1] = mask[:x, y:y + 1]
            new_mask[x:, y:y + 1] = mask[x + 1:, y:y + 1]

        stitchMask[x, y] = 1

        return [result, new_mask, stitchMask]

    if mode == "horizontal expand":
        stitch[0:1, :] = gradient[0:1, :]

        for i in range(1, height):
            for j in range(0, width):
                min_neighbour = stitch[i - 1, j]
                if j != 0 and stitch[i - 1, j - 1] < min_neighbour:
                    min_neighbour = stitch[i - 1, j - 1]
                if j != width - 1 and stitch[i - 1, j + 1] < min_neighbour:
                    min_neighbour = stitch[i - 1, j + 1]
                stitch[i, j] = gradient[i, j] + min_neighbour

        x = height - 1
        y = np.argmin(stitch[x:, :])

        result = np.zeros([height, width + 1, 3])
        stitchMask = np.zeros([height, width])

        if mask is not None:
            new_mask = np.zeros([height, width + 1])
        else:
            new_mask = mask

        while x != 0:
            result[x:x + 1, :y + 1, :] = img[x:x + 1, :y + 1, :]
            result[x:x + 1, y + 2:, :] = img[x:x + 1, y + 1:, :]

            if y == width - 1:
                result[x:x + 1, y + 1:y + 2, :] = img[x:x + 1, y:y + 1, :]
            else:
                result[x:x + 1, y + 1:y + 2, :] = (img[x:x + 1, y:y + 1, :] + img[x:x + 1, y + 1:y + 2, :]) * 0.5

            if mask is not None:
                new_mask[x:x + 1, :y + 1] = mask[x:x + 1, :y + 1]
                new_mask[x:x + 1, y + 2:] = mask[x:x + 1, y + 1:]

                if y == width - 1:
                    new_mask[x:x + 1, y + 1:y + 2] = mask[x:x + 1, y:y + 1]
                else:
                    new_mask[x:x + 1, y + 1:y + 2] = (mask[x:x + 1, y:y + 1] + mask[x:x + 1, y + 1:y + 2]) // 2

            stitchMask[x, y] = 1

            x -= 1

            min_neighbour = (stitch[x, y], 0)
            if y != 0 and stitch[x, y - 1] <= min_neighbour[0]:
                min_neighbour = (stitch[x, y - 1], -1)
            if y != width - 1 and stitch[x, y + 1] < min_neighbour[0]:
                min_neighbour = (stitch[x, y + 1], 1)
            y = y + min_neighbour[1]

        result[x:x + 1, :y + 1, :] = img[x:x + 1, :y + 1, :]
        result[x:x + 1, y + 2:, :] = img[x:x + 1, y + 1:, :]

        if y == width - 1:
            result[x:x + 1, y + 1:y + 2, :] = img[x:x + 1, y:y + 1, :]
        else:
            result[x:x + 1, y + 1:y + 2, :] = (img[x:x + 1, y:y + 1, :] + img[x:x + 1, y + 1:y + 2, :]) * 0.5

        if mask is not None:
            new_mask[x:x + 1, :y + 1] = mask[x:x + 1, :y + 1]
            new_mask[x:x + 1, y + 2:] = mask[x:x + 1, y + 1:]

            if y == width - 1:
                new_mask[x:x + 1, y + 1:y + 2] = mask[x:x + 1, y:y + 1]
            else:
                new_mask[x:x + 1, y + 1:y + 2] = (mask[x:x + 1, y:y + 1] + mask[x:x + 1, y + 1:y + 2]) // 2

        stitchMask[x, y] = 1

        return [result, new_mask, stitchMask]

    if mode == "vertical expand":
        stitch[:, 0:1] = gradient[:, 0:1]

        for j in range(1, width):
            for i in range(0, height):
                min_neighbour = stitch[i, j - 1]
                if i != 0 and stitch[i - 1, j - 1] < min_neighbour:
                    min_neighbour = stitch[i - 1, j - 1]
                if i != height - 1 and stitch[i + 1, j - 1] < min_neighbour:
                    min_neighbour = stitch[i + 1, j - 1]
                stitch[i, j] = gradient[i, j] + min_neighbour

        y = width - 1
        x = np.argmin(stitch[:, y:])

        result = np.zeros([height + 1, width, 3])
        stitchMask = np.zeros([height, width])

        if mask is not None:
            new_mask = np.zeros([height + 1, width])
        else:
            new_mask = mask

        while y != 0:
            result[:x + 1, y:y + 1, :] = img[:x + 1, y:y + 1, :]
            result[x + 2:, y:y + 1, :] = img[x + 1:, y:y + 1, :]

            if x == height - 1:
                result[x + 1:x + 2, y:y + 1, :] = img[x:x + 1, y:y + 1, :]
            else:
                result[x + 1:x + 2, y:y + 1, :] = (img[x:x + 1, y:y + 1, :] + img[x + 1:x + 2, y:y + 1, :]) * 0.5

            if mask is not None:
                new_mask[:x + 1, y:y + 1] = mask[:x + 1, y:y + 1]
                new_mask[x + 2:, y:y + 1] = mask[x + 1:, y:y + 1]

                if x == height - 1:
                    new_mask[x + 1:x + 2, y:y + 1] = mask[x:x + 1, y:y + 1]
                else:
                    new_mask[x + 1:x + 2, y:y + 1] = (mask[x:x + 1, y:y + 1] + mask[x + 1:x + 2, y:y + 1]) // 2

            stitchMask[x, y] = 1

            y -= 1

            min_neighbour = (stitch[x, y], 0)
            if x != 0 and stitch[x - 1, y] <= min_neighbour[0]:
                min_neighbour = (stitch[x - 1, y], -1)
            if x != height - 1 and stitch[x + 1, y] < min_neighbour[0]:
                min_neighbour = (stitch[x + 1, y], 1)
            x = x + min_neighbour[1]

        result[:x + 1, y:y + 1, :] = img[:x + 1, y:y + 1, :]
        result[x + 2:, y:y + 1, :] = img[x + 1:, y:y + 1, :]

        if x == height - 1:
            result[x + 1:x + 2, y:y + 1, :] = img[x:x + 1, y:y + 1, :]
        else:
            result[x + 1:x + 2, y:y + 1, :] = (img[x:x + 1, y:y + 1, :] + img[x + 1:x + 2, y:y + 1, :]) * 0.5

        if mask is not None:
            new_mask[:x + 1, y:y + 1] = mask[:x + 1, y:y + 1]
            new_mask[x + 2:, y:y + 1] = mask[x + 1:, y:y + 1]

            if x == height - 1:
                new_mask[x + 1:x + 2, y:y + 1] = mask[x:x + 1, y:y + 1]
            else:
                new_mask[x + 1:x + 2, y:y + 1] = (mask[x:x + 1, y:y + 1] + mask[x + 1:x + 2, y:y + 1]) // 2

        stitchMask[x, y] = 1

        return [result, new_mask, stitchMask]