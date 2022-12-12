from maya import cmds


def pivot_to_origin(obj):
    """
    set the pivot of the object to the origin of the scene in worldspace and
    freezes the tranformation
    :param obj: takes the name of the  object
    :return: none
    """
    cmds.move(0, 0, 0, f"{obj}.scalePivot", f'{obj}.rotatePivot', absolute=True)
    cmds.makeIdentity(apply=True)

