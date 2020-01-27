def get_projection(points, axe):
    max_point = axe.dot(points[0])
    min_point = axe.dot(points[0])

    for point in points:
        max_point = max(max_point, axe.dot(point))
        min_point = min(min_point, axe.dot(point))

    return min_point, max_point

def overlap(projection1, projection2):
    if projection1[0] <= projection2[0] <= projection1[1]:
        return True
    elif projection1[0] <= projection2[1] <= projection1[1]:
        return True
    elif projection2[0] <= projection1[0] <= projection2[1]:
        return True
    elif projection2[0] <= projection1[1] <= projection2[1]:
        return True
    else:
        return False


def rectangles_colision(rectangle1, rectangle2):
    axis = rectangle1.separating_axis + rectangle2.separating_axis

    for axe in axis:
        projection1 = get_projection(rectangle1.corners, axe)
        projection2 = get_projection(rectangle2.corners, axe)

        if not overlap(projection1, projection2):
            return False

    return True

