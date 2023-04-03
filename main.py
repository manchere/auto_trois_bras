"""
AutoTroisBras
Manu Cheremeh, Version 1.0, July 2022
@author = Manu Cheremeh
version = 1.0
"""

from maya import cmds

import maya.api.OpenMaya as om
from PySide2 import QtWidgets
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

from maya import mel as mel
from functools import reduce

from cv_data import CONTROL_CURVES, CUBE_CURVES_DATA
from lib.ctrl_curves import ControlCurve
from lib.computation.manipulation import *
from lib.styleSheet import *

CONTROL_CURVES = {
    'four_arrow': 'curve -d 1 -p -1 0 -1 -p -1 0 -3 -p -2 0 -3 -p 0 0 -5 -p 2 0 -3 -p 1 0 -3 -p 1 0 -1 -p 3 0 -1 -p 3 0'
                  '-2 -p 5 0 0 -p 3 0 2 -p 3 0 1 -p 1 0 1 -p 1 0 3 -p 2 0 3 -p 0 0 5 -p -2 0 3 -p -1 0 3 -p -1 0 1 '
                  '-p -3 0 1 -p -3 0 2 -p -5 0 0 -p -3 0 -2 -p -3 0 -1 -p -1 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 '
                  '-k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k '
                  '23 -k 24 ;',
    'two_arrow': 'curve -d 1 -p 100 -20 0 -p 20 -20 0 -p 20 0 0 -p -20 -40 0 -p 20 -80 0 -p 20 -60 0 -p 100 -60 0 -p 100 -80 0 -p 140 -40 0 -p 100 0 0 -p 100 -20 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 ;',
    'circle_legacy': 'circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1; objectMoveCommand;',
    'circle': 'circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 1e-08 -s 8 -ch 1; objectMoveCommand;',
    'square': 'curve -d 1 -p 2 0 -2 -p -2 0 -2 -p -2 0 2 -p 2 0 2 -p 2 0 -2 -k 0 -k 1 -k 2 -k 3 -k 4 ;',
    'cube_square': 'curve -d 1 -p 2 0 -2 -p -2 0 -2 -p -2 0 2 -p 2 0 2 -p 2 0 -2 -k 0 -k 1 -k 2 -k 3 -k 4 ;',
    'F': 'curve -d 1 -p 0 0 0 -p 0 100 0 -p 80 100 0 -p 80 80 0 -p 20 80 0 -p 20 60 0 -p 60 60 0 -p 60 40 0 -p 20 40 0 -p 20 0 0 -p 0 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 ;',
    'K': 'curve -d 1 -p 0 100 0 -p 0 0 0 -p 20 0 0 -p 20 40 0 -p 60 0 0 -p 80 0 0 -p 40 40 0 -p 40 60 0 -p 80 100 0 -p 60 100 0 -p 20 60 0 -p 20 100 0 -p 0 100 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 ;',
    'I': 'curve -d 1 -p 20 100 0 -p 0 100 0 -p 0 0 0 -p 20 0 0 -p 20 100 0 -k 0 -k 1 -k 2 -k 3 -k 4 ;',
    'three_circles': 'circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 1e-08 -s 8 -ch 1; objectMoveCommand;'
                     'scale -r 3 3 3 ;'
                     'duplicate -rr;'
                     'rotate -r -os -fo -90 0 0 ;'
                     'duplicate -rr;'
                     'rotate -r -os -fo 0 0 -90 ;'
                     'select -r nurbsCircle1 nurbsCircle2 nurbsCircle3 ;'
                     'makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;'
                     'select -r nurbsCircleShape3 ;'
                     'select -add nurbsCircleShape2 ;'
                     'select -add nurbsCircleShape1 ;'
                     'select -add nurbsCircle1 ;'
                     'parent -r -s;'
                     'select -r nurbsCircle1'
}

CUBE_CURVES_DATA = {
    'cube': 'polyCube -n ref_cube -w 10 -h 10 -d 10 -sx 1 -sy 1 -sz 1 -ax 0 1 0 -cuv 4 -ch 1;'
}


def get_main_window():
    """Get the maya window pointer to parent the main window inside maya"""
    ptr = omui.MQtUtil.mainWindow()
    maya_window = wrapInstance(int(ptr), QtWidgets.QWidget)
    return maya_window


class ControlCurve:

    @staticmethod
    def curve_ctrl(cv_name, cv_type='circle'):
        cv = mel.eval(CONTROL_CURVES[cv_type])
        cmds.rename(cv, cv_name)
        cmds.scale(10, 10, 10, ws=True, r=True)
        cmds.select(cv_name + '.cv[0:7]', r=True)
        cmds.rotate(0, 0, 90, r=True, p=[0, 0, 0], os=True)
        cmds.makeIdentity(a=True, t=True, r=True, s=True, n=False)
        cmds.select(cl=True)

        return cv_name

    def cube_ctrl(self, name):
        ref_cube = mel.eval(CUBE_CURVES_DATA['cube'])
        curvesShape = []
        for i in range(12):
            cmds.select('ref_cube.e[{id}]'.format(id=i), r=True)
            curvesShape.append(cmds.listRelatives(cmds.polyToCurve()[0], type='nurbsCurve')[0])
            cmds.select(cl=True)
        cmds.rename(cmds.listRelatives(curvesShape[0], p=True), name)
        curvesShape.remove(curvesShape[0])
        self._parent_ctrl(name, curvesShape)
        cmds.delete('ref_cube')

        return name

    @staticmethod
    def pole_ctrl(cv_name, cv_type='four_arrow'):
        cv = mel.eval(CONTROL_CURVES[cv_type])
        cmds.rename(cv, cv_name)
        # cmds.scale(, 2.5, 2.5, ws=True, r=True)
        cmds.select(cv_name + '.cv[0:24]', r=True)
        cmds.makeIdentity(a=True, t=True, r=True, s=True, n=False)
        cmds.select(cl=True)
        return cv_name

    @staticmethod
    def three_circle_ctrl(cv_name, cv_type):
        cv = mel.eval(CONTROL_CURVES[cv_type])
        cmds.rename(cv, cv_name)
        cmds.makeIdentity(a=True, t=True, r=True, s=True, n=False)
        cmds.select(cl=True)
        return cv_name

    @staticmethod
    def _parent_ctrl(ctrl_name, shapes):
        for i in shapes:
            cmds.parent(i, ctrl_name, r=True, s=True)

    def transform_ctrl(self):
        pass

    def constraint_ctrl(self):
        pass


class Control:
    def __init__(self, parent_joint, end_joint):
        self.parent_joint = parent_joint
        self.end_joint = end_joint
        self.joints = None
        self.fk_controls = []
        self.ik_controls = []
        self.ik_pole_control = ''
        self.ik_handle = None
        self.ik_effector = None

    def get_proper_chain(self):
        if self.parent_joint or (self.parent_joint and self.end_joint):
            children_joints = self.get_joint_chain(self.parent_joint)
            end_joint_chain = self.get_joint_chain(self.end_joint)

            neat_children_list = [item for item in children_joints if item not in end_joint_chain]
            return neat_children_list + [self.parent_joint]

    @staticmethod
    def get_joint_chain(joint):
        """
        returns the joints after a specific joint
        :param joint: the name of the specific joint
        :return list of joint
        """
        chain = cmds.listRelatives(joint, ad=True, type='joint')
        if chain:
            return chain
        return []

    def set_fk_controls(self):
        self.joints = self.get_proper_chain()
        for idx, joint in enumerate(self.joints):
            ctrl = ControlCurve()
            ctrl_curve = ctrl.curve_ctrl(joint + '_FK_CTRL', 'circle')
            cmds.matchTransform(ctrl_curve, joint, pos=True, rot=True, scale=False)
            cmds.orientConstraint(ctrl_curve, joint)
            self.fk_controls.append(ctrl_curve)

    def parent_fk_controls(self):
        for idx, ctrl in enumerate(self.fk_controls[:-1]):
            cmds.parent(ctrl, self.fk_controls[idx + 1])
            bake_t_opmatrix(ctrl)
        bake_t_opmatrix(self.fk_controls[-1])

    def set_ik_controls(self):
        self.ik_handle, self.ik_effector = cmds.ikHandle(name=self.parent_joint + '_IK', sj=self.parent_joint,
                                                         ee=self.end_joint, solver='ikRPsolver')
        ctrl = ControlCurve()
        ctrl_cube = ctrl.cube_ctrl(self.end_joint + '_IK_CTRL')
        cmds.matchTransform(ctrl_cube, self.end_joint, pos=True, rot=True, scale=False)
        cmds.pointConstraint(ctrl_cube, self.ik_handle)
        cmds.orientConstraint(ctrl_cube, self.end_joint)
        self.ik_controls.append(ctrl_cube)
        bake_t_opmatrix(self.ik_controls[0])
        self.set_ik_pole_control(-90)

    def set_ik_pole_control(self, offset):
        ctrl = ControlCurve()
        self.ik_pole_control = ctrl.three_circle_ctrl(self.parent_joint + '_IK_CTRL', 'three_circles')
        cmds.xform(self.ik_pole_control,
                   t=self._get_pv_position(),
                   ws=True)
        # cmds.matchTransform(self.ik_pole_control, self.parent_joint, rx=True)
        bake_t_opmatrix(self.ik_pole_control)
        cmds.poleVectorConstraint(self.ik_pole_control, self.ik_handle)

    def _get_mid_point(self):
        root_vector = cmds.xform(self.parent_joint, ws=True, q=True, rp=True, t=True)
        end_vector = cmds.xform(self.end_joint, ws=True, q=True, rp=True, t=True)

        x = (root_vector[0] + end_vector[0]) / 2.0
        y = (root_vector[1] + end_vector[1]) / 2.0
        z = (root_vector[2] + end_vector[2]) / 2.0
        return x, y, z

    def _get_pv_position(self):
        parent_pos = om.MVector(cmds.xform(self.joints[0], q=True, rp=True, ws=True))
        print(parent_pos)


        mid_pos = om.MVector(cmds.xform(self.joints[1], q=True, rp=True, ws=True))
        end_pos = om.MVector(cmds.xform(self.joints[2], q=True, rp=True, ws=True))

        parent_to_end = parent_pos - end_pos
        parent_to_end_scaled = parent_to_end * 0.5
        mid_point = parent_pos + parent_to_end_scaled

        mm_vec = mid_pos - mid_point
        cmds.xform(cmds.spaceLocator(), ws=True, t=mm_vec)
        mm_vec_scaled = mm_vec * 2
        cmds.xform(cmds.spaceLocator(), ws=True, t=mm_vec_scaled)
        mid_point_to_pos = mid_point + mm_vec_scaled
        cmds.xform(cmds.spaceLocator(), ws=True, t=mid_point_to_pos)

        return mid_point_to_pos


    @staticmethod
    def _vec_mean(ls):
        x = 0
        y = 0
        z = 0
        for i in ls:
            print(ls)
            x += i[0]
            y += i[1]
            z += i[2]
        return [x/len(ls), y/len(ls), z/len(ls)]

    def _set_pv_location(self):
        pass

    def build(self):
        self.set_fk_controls()
        self.parent_fk_controls()
        self.set_ik_controls()


class IkFkSwitch:
    def __init__(self, ik_handle, ik_ctrl, fk_parent_ctrl):
        self.ik_handle = ik_handle
        self.ik_ctrl = ik_ctrl
        self.fk_parent_ctrl = fk_parent_ctrl

    @staticmethod
    def _prep_ctrl(ctrl, tx, ty):
        cmds.xform(ctrl, cp=True)
        cmds.matchTransform(ctrl, cmds.spaceLocator('guidor'))
        cmds.scale(0.125, 0.125, 0.125, ctrl)
        cmds.makeIdentity(a=True, t=True, r=True, s=True, n=False)
        cmds.move(ctrl, tx, ty, xy=True)
        for i in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']:
            cmds.setAttr("ctrl.{n}".format(n=i), lock=True, keyable=False, channelBox=False)

        cmds.delete('guidor')

    def create_ikfk(self):
        pass

    def connect_ikfk(self):
        pass

    def switch_to_fk(self):
        cmds.setAttr(self.switch_attr, 1)

        # Hide the IK handle
        cmds.hide(self.ik_handle)
        cmds.hide(self.ik_effector)

        # Show the FK controls
        for control in self.fk_controls:
            cmds.showHidden(control)

    def switch_to_ik(self):
        cmds.setAttr(self.switch_attr, 0)

        # Show the IK handle
        cmds.showHidden(self.ik_handle)
        cmds.showHidden(self.ik_effector)

        # Hide the FK controls
        for control in self.fk_controls:
            cmds.hide(control)


class Main(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.main_widget = QtWidgets.QWidget(self)
        self.ver_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.first_row = QtWidgets.QHBoxLayout()
        self.sec_row = QtWidgets.QHBoxLayout()
        self.txt_parent_joint = QtWidgets.QLineEdit()
        self.txt_end_joint = QtWidgets.QLineEdit()
        self.lbl_parent = QtWidgets.QLabel('Parent Joint')
        self.lbl_end = QtWidgets.QLabel('End Joint')
        self.btn_parent_joint = QtWidgets.QPushButton('parent joint')
        self.btn_end_joint = QtWidgets.QPushButton('end joint')
        self.btn_create_system = QtWidgets.QPushButton("create system")

        self.style = Style(self.main_widget)

        self.setObjectName('auto_trois_bras')

        self.setWindowTitle('Auto 3 Bras')
        self.setGeometry(450, 300, 300, 150)

        self.setCentralWidget(self.main_widget)

        self.first_row.addWidget(self.txt_parent_joint, 7)
        self.first_row.addWidget(self.btn_parent_joint, 3)

        self.sec_row.addWidget(self.txt_end_joint, 7)
        self.sec_row.addWidget(self.btn_end_joint, 3)

        self.ver_layout.addLayout(self.first_row)
        self.ver_layout.addLayout(self.sec_row)
        self.ver_layout.addWidget(self.btn_create_system)

        self.btn_parent_joint.clicked.connect(self.add_parent_joint)
        self.btn_end_joint.clicked.connect(self.add_end_joint)

        self.btn_create_system.clicked.connect(self.create_system)

    def add_parent_joint(self):
        self.txt_parent_joint.setText(cmds.ls(sl=True)[0])

    def add_end_joint(self):
        self.txt_end_joint.setText(cmds.ls(sl=True)[0])

    def create_system(self):
        control = Control(self.txt_parent_joint.text(), self.txt_end_joint.text())
        control.build()


TRANSFORM_NODETYPES = ['transform', 'joint']


def has_non_default_locked_attributes(node):
    locked_attributes = []
    for attribute in ["translate", "rotate", "scale", "jointOrient"]:
        default_value = 1 if attribute == "scale" else 0
        for axis in "XYZ":
            if cmds.attributeQuery(attribute + axis, node=node, exists=True):
                attribute_name = "{}.{}{}".format(node, attribute, axis)
                current_value = cmds.getAttr(attribute_name)
                if cmds.getAttr(attribute_name, lock=True) and current_value != default_value:
                    return True


def reset_transforms(node):
    for attribute in ["translate", "rotate", "scale", "jointOrient"]:
        value = 1 if attribute == "scale" else 0
        for axis in "XYZ":
            if cmds.attributeQuery(attribute + axis, node=node, exists=True):
                attribute_name = "{}.{}{}".format(node, attribute, axis)
                if not cmds.getAttr(attribute_name, lock=True):
                    cmds.setAttr(attribute_name, value)


def bake_t_opmatrix(node):
    if cmds.nodeType(node) not in TRANSFORM_NODETYPES:
        raise ValueError("Node {} is not a transform node".format(node))

    if has_non_default_locked_attributes(node):
        raise RuntimeError("Node {} has at least one non default locked attribute(s)".format(node))

    local_matrix = om.MMatrix(cmds.xform(node, q=True, m=True, ws=False))
    offset_parent_matrix = om.MMatrix(cmds.getAttr(node + ".offsetParentMatrix"))
    baked_matrix = local_matrix * offset_parent_matrix
    cmds.setAttr(node + ".offsetParentMatrix", baked_matrix, type="matrix")

    reset_transforms(node)


if __name__ == '__main__':
    main_window = get_main_window()
    tool = Main(main_window)
    tool.show()
