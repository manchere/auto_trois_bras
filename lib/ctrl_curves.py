from maya import cmds as cmds
from pymel import core as pm
from maya import mel as mel

# from computation.manipulation import pivot_to_origin
from cv_data import CONTROL_CURVES, CUBE_CURVES_DATA


class ControlCurve:

    def __init__(self):
        print('hello i got here')
        pass

    @staticmethod
    def __bake_ctrl(name, **kwargs):
        cmds.xform(name, ws=True, **kwargs)
        # pivot_to_origin(name)

    @staticmethod
    def curve_ctrl(cv_name, cv_type='circle'):
        cv = mel.eval(CONTROL_CURVES[cv_type])
        cmds.rename(cmds.select(cv), cv_name)

    @staticmethod
    def cube_ctrl(self, name):
        for key, data in enumerate(CUBE_CURVES_DATA):
            self.create_ctrl_curves(key, cv_type='cube_line')
            self.__bake_ctrl(name, t=data)

    def transform_ctrl(self):
        pass

    def constraint_ctrl(self):
        pass

    def bake_ctrl(self):
        pass