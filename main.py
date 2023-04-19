"""
AutoTroisBras
Manu Cheremeh, Version 1.0, July 2022
@author = Manu Cheremeh
version = 1.0
"""

from maya import cmds

import maya.api.OpenMaya as om
from PySide2 import QtWidgets, QtCore
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

from maya import mel as mel
from functools import partial

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
    def ikfk_ctrl(name):
        i = cmds.rename(mel.eval(CONTROL_CURVES['I']), 'i_' + name)
        cmds.scale(0.08, 0.08, 0.08)
        cmds.move(0, 0.6, 0)
        f = cmds.rename(mel.eval(CONTROL_CURVES['F']), 'f_' + name)
        cmds.scale(0.08, 0.08, 0.08)
        cmds.move(0, 0.6, 0)
        k = cmds.rename(mel.eval(CONTROL_CURVES['K']), 'k_' + name)
        cmds.scale(0.08, 0.08, 0.08)
        cmds.move(7, 0.6, 0)
        arrow = mel.eval(CONTROL_CURVES['two_arrow'])
        cmds.scale(0.1, 0.1, 0.1)
        cmds.rename(arrow, name)
        for ctrl in [i, f, k]:
            cmds.parent(ctrl, name)
            cmds.rotate(0, 0, 0, r=True, p=[0, 0, 0], os=True)
            cmds.select(ctrl, add=True)
            cmds.makeIdentity(a=True, t=True, r=True, s=True, n=False)
        return {'i': i, 'f': f, 'k': k, 'name': name}


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


class Control:
    def __init__(self, parent_joint, end_joint):
        self.parent_joint = parent_joint
        self.end_joint = end_joint
        self.joints = None
        self.fk_controls = []
        self.ik_control = ''
        self.ik_pole_control = ''
        self.ik_handle = None
        self.ik_effector = None
        self.switch_control = None
        self.ikfk_switch_control = None
        self.end_orient_constraint = None

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

    def get_proper_chain(self):
        if self.parent_joint or (self.parent_joint and self.end_joint):
            children_joints = self.get_joint_chain(self.parent_joint)
            end_joint_chain = self.get_joint_chain(self.end_joint)

            neat_children_list = [item for item in children_joints if item not in end_joint_chain]
            return neat_children_list + [self.parent_joint]

    def set_fk_controls(self, inc_end_joint='include'):
        self.joints = self.get_proper_chain()
        self.joints.pop(0) if inc_end_joint == 'exclude' else self.joints
        for idx, joint in enumerate(self.joints):
            ctrl = ControlCurve()
            ctrl_curve = ctrl.curve_ctrl(joint + '_FK_CTRL', 'circle')
            cmds.matchTransform(ctrl_curve, joint, pos=True, rot=True, scale=False)
            cmds.orientConstraint(ctrl_curve, joint)
            self.fk_controls.append(ctrl_curve)
        self._parent_fk_controls()

    def _parent_fk_controls(self):
        for idx, ctrl in enumerate(self.fk_controls[:-1]):
            cmds.parent(ctrl, self.fk_controls[idx + 1])
            bake_t_opmatrix(ctrl)
        bake_t_opmatrix(self.fk_controls[-1])

    def set_ik_controls(self):
        self.ik_handle, self.ik_effector = cmds.ikHandle(name=self.parent_joint + '_IK', sj=self.parent_joint,
                                                         ee=self.end_joint, solver='ikRPsolver')
        ctrl = ControlCurve()
        self.ik_control = ctrl.cube_ctrl(self.end_joint + '_IK_CTRL')
        cmds.matchTransform(self.ik_control, self.end_joint, pos=True, rot=True, scale=False)
        cmds.pointConstraint(self.ik_control, self.ik_handle)
        self.end_orient_constraint = cmds.orientConstraint(self.ik_control, self.end_joint)
        bake_t_opmatrix(self.ik_control)
        self.set_ik_pole_control()

    def set_ik_pole_control(self):
        ctrl = ControlCurve()
        self.ik_pole_control = ctrl.three_circle_ctrl(self.parent_joint + '_IK_CTRL', 'three_circles')
        cmds.xform(self.ik_pole_control, t=self._get_pv_position())
        bake_t_opmatrix(self.ik_pole_control)
        cmds.poleVectorConstraint(self.ik_pole_control, self.ik_handle)

    def set_ik_switch_control(self):
        ctrl = ControlCurve()
        self.ikfk_switch_control = ctrl.ikfk_ctrl(self.end_joint + '_ikfk_switch')
        cmds.matchTransform(self.ikfk_switch_control['name'], self.end_joint, pos=True)
        cmds.pointConstraint(self.end_joint, self.ikfk_switch_control['name'], o=[0, 10, 0])
        self.switch_control = self.ikfk_switch_control['name']

    @staticmethod
    def _get_mid_point(ls):
        sum_vec = om.MVector()
        for i in ls:
            sum_vec += om.MVector(cmds.xform(i, q=True, rp=True, ws=True))
        return sum_vec / len(ls)

    def _get_pv_position(self):
        self.joints = self.get_proper_chain()
        sum_point = om.MVector()
        for i in range(len(self.joints[:-2])):
            parent_pos = om.MVector(cmds.xform(self.joints[i + 2], q=True, rp=True, ws=True))
            end_pos = om.MVector(cmds.xform(self.joints[i], q=True, rp=True, ws=True))
            mid_pos = om.MVector(cmds.xform(self.joints[i + 1], q=True, rp=True, ws=True))

            parent_to_end = end_pos - parent_pos
            parent_end_scaled = parent_to_end * 0.5
            mid_point = parent_pos + parent_end_scaled
            mm_vec = mid_pos - mid_point
            mid_point_elbow_vec_scaled = mm_vec * 3

            mm_point = mid_point + mid_point_elbow_vec_scaled

            sum_point += mm_point
        return sum_point / len(self.joints[:-2])

    def _mid_avg(self, ls):
        if len(ls) > 3:
            return self._get_mid_point(ls)
        return ls[1]

    @staticmethod
    def _vec_mean(ls):
        x = 0
        y = 0
        z = 0
        for i in ls:
            x += i[0]
            y += i[1]
            z += i[2]
        return [x / len(ls), y / len(ls), z / len(ls)]

    def _set_pv_location(self):
        pass


class IkFkSwitch(Control):
    # def __init__(self, ik_handle, ik_ctrl, pv_ctrl, fk_parent_ctrl, switch_ctrl, parent_joint, end_joint):
    def __init__(self, parent_joint, end_joint):
        super().__init__(parent_joint, end_joint)
        self.tool = Tools()

    @staticmethod
    def _lock_ctrl(ctrl, attr_list):
        cmds.xform(ctrl, cp=True)
        for i in attr_list:
            cmds.setAttr(ctrl + "." + i, lock=True, keyable=False, channelBox=False)

    def add_ikfk(self):
        attr = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
        self._lock_ctrl(self.switch_control, attr)
        self._lock_ctrl(self.switch_control, ['visibility'])
        cmds.select(self.switch_control)
        cmds.addAttr(shortName='ikfk', longName='IK_FK_Blend', defaultValue=1.0, minValue=0.0, maxValue=1.0)
        cmds.setAttr('.IK_FK_Blend', e=True, keyable=True)
        for x in cmds.listRelatives(self.switch_control, ad=True, type='transform'):
            self._lock_ctrl(x, attr)
            self._lock_ctrl(x, ['visibility']) if x not in [self.ikfk_switch_control['i'], self.ikfk_switch_control['f']] else print(x)

    def _connect_ikfk(self):
        cmds.setDrivenKeyframe(self.ik_handle + '.ikBlend', cd=self.switch_control + '.IK_FK_Blend')
        cmds.setDrivenKeyframe(self.fk_controls[-1] + '.visibility', cd=self.switch_control + '.IK_FK_Blend')
        cmds.setDrivenKeyframe(self.ik_control + '.visibility', cd=self.switch_control + '.IK_FK_Blend')
        cmds.setDrivenKeyframe(self.ik_pole_control + '.visibility', cd=self.switch_control + '.IK_FK_Blend')
        cmds.setDrivenKeyframe(self.ikfk_switch_control['f'] + '.visibility', cd=self.switch_control + '.IK_FK_Blend')
        cmds.setDrivenKeyframe(self.ikfk_switch_control['i'] + '.visibility', cd=self.switch_control + '.IK_FK_Blend')
        cmds.setDrivenKeyframe(self.end_orient_constraint[0] + '.' + self.ik_control + 'W0',
                               cd=self.switch_control + '.IK_FK_Blend')
        cmds.setDrivenKeyframe(self.end_orient_constraint[0] + '.' + self.fk_controls[0] + 'W1', cd=self.switch_control + '.IK_FK_Blend')

    def _switch_to_fk(self):
        cmds.setAttr(self.switch_control + '.IK_FK_Blend', 0.0)
        cmds.setAttr(self.ik_handle + '.ikBlend', 0)
        cmds.setAttr(self.end_orient_constraint[0] + '.' + self.ik_control + 'W0', 0)
        cmds.setAttr(self.end_orient_constraint[0] + '.' + self.fk_controls[0] + 'W1', 1)
        cmds.hide(self.ik_control)
        cmds.hide(self.ikfk_switch_control['i'])
        cmds.hide(self.ik_pole_control)
        cmds.showHidden(self.fk_controls[-1])
        cmds.showHidden(self.ikfk_switch_control['f'])

    def _switch_to_ik(self):
        cmds.setAttr(self.switch_control + '.IK_FK_Blend', 1.0)
        cmds.setAttr(self.ik_handle + '.ikBlend', 1.0)
        cmds.setAttr(self.end_orient_constraint[0] + '.' + self.ik_control + 'W0', 1)
        cmds.setAttr(self.end_orient_constraint[0] + '.' + self.fk_controls[0] + 'W1', 0)
        cmds.hide(self.fk_controls[-1])
        cmds.hide(self.ikfk_switch_control['f'])
        cmds.showHidden(self.ik_pole_control)
        cmds.showHidden(self.ik_control)
        cmds.showHidden(self.ikfk_switch_control['i'])

    @staticmethod
    def set_color(ctrl, color=(1, 0, 1)):
        rgb = ("R", "G", "B")
        cmds.setAttr(ctrl + ".overrideEnabled", 1)
        cmds.setAttr(ctrl + ".overrideRGBColors", 1)
        for channel, color in zip(rgb, color):
            cmds.setAttr(ctrl + ".overrideColor%s" % channel, color)

    def assign_color(self, ctrls, color):
        for i in ctrls:
            self.set_color(i, color)

    def build_ikfk(self):
        self.set_ik_switch_control()
        self.add_ikfk()
        self._switch_to_ik()
        self._connect_ikfk()
        self._switch_to_fk()
        self._connect_ikfk()
        Tools.clean_output()

    def build(self, build_type, inc_end_joint='include', colors=None):
        if build_type == 0:
            self.set_ik_controls()
            self.set_fk_controls(inc_end_joint)
            self.build_ikfk()
            self.assign_color([self.ik_control, self.ik_pole_control], colors['ik'])
            self.assign_color(self.fk_controls, colors['fk'])
            self.assign_color([self.ikfk_switch_control['f']], colors['fk'])
            self.assign_color([self.ikfk_switch_control['i']], colors['ik'])
            self.assign_color([self.ikfk_switch_control['k']], [1, 1, 1])
            self.assign_color([self.ikfk_switch_control['name']], [1, 1, 1])
        elif build_type == 1:
            self.set_fk_controls(inc_end_joint)
            self.assign_color(self.fk_controls, colors['fk'])
        else:
            self.set_ik_controls()
            self.assign_color([self.ik_control, self.ik_pole_control], colors['ik'])
        self.tool.clean_output()
        self.tool.group_ctrl(self.ik_control+'ik_grp', [self.ik_control, self.ik_pole_control])


class Tools:

    @staticmethod
    def clean_output():
        deleteList = []
        for tran in cmds.ls(type='transform'):
            if cmds.nodeType(tran) == 'transform':
                children = cmds.listRelatives(tran, c=True)
                if children is None:
                    deleteList.append(tran)

        if len(deleteList) > 0:
            cmds.delete(deleteList)

    @staticmethod
    def group_ctrl(name, ls):
        grpname = cmds.group(n=name)
        for cur_name in ls:
            cmds.parent(cur_name, grpname)


class Main(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.fk_color = [1, 0, 0]
        self.ik_color = [0, 1, 0]
        self.main_widget = QtWidgets.QWidget(self)
        self.ver_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.choice_row = QtWidgets.QHBoxLayout()
        self.first_row = QtWidgets.QHBoxLayout()
        self.sec_row = QtWidgets.QHBoxLayout()
        self.third_row = QtWidgets.QHBoxLayout()
        self.fourth_row = QtWidgets.QHBoxLayout()
        self.txt_parent_joint = QtWidgets.QLineEdit()
        self.txt_end_joint = QtWidgets.QLineEdit()
        self.lbl_parent = QtWidgets.QLabel('Parent Joint')
        self.lbl_end = QtWidgets.QLabel('End Joint')
        self.lbl_type = QtWidgets.QLabel('Type:')
        self.btn_parent_joint = QtWidgets.QPushButton('parent joint')
        self.btn_end_joint = QtWidgets.QPushButton('end joint')
        self.cmb_control_type = QtWidgets.QComboBox()
        self.radio_end_fk_control = QtWidgets.QCheckBox('Include FK control on end joint')
        self.btn_create_system = QtWidgets.QPushButton("create system")
        self.btn_color_fk = QtWidgets.QPushButton('FK')
        self.btn_color_ik = QtWidgets.QPushButton('IK')

        self.style = Style(self.main_widget)

        self.setObjectName('auto_trois_bras')

        self.setWindowTitle('Auto 3 Bras')
        self.setGeometry(450, 300, 300, 150)

        self.setCentralWidget(self.main_widget)

        self.btn_color_ik.setStyleSheet('QPushButton {background-color: green; color: white;}')
        self.btn_color_fk.setStyleSheet('QPushButton {background-color: red; color: white;}')
        self.btn_parent_joint.setStyleSheet('QPushButton {background-color: #1d2951; color: white;}')
        self.btn_end_joint.setStyleSheet('QPushButton {background-color: #1d2951 ; color: white;}')
        self.btn_create_system.setStyleSheet('QPushButton {background-color: #1d2951; color: gray;}')

        self.cmb_control_type.addItems(['IK / FK', 'IK only', 'FK only'])

        self.choice_row.addWidget(self.lbl_type, 3)
        self.choice_row.addWidget(self.cmb_control_type, 7)
        self.first_row.addWidget(self.txt_parent_joint, 7)
        self.first_row.addWidget(self.btn_parent_joint, 3)

        self.sec_row.addWidget(self.txt_end_joint, 7)
        self.sec_row.addWidget(self.btn_end_joint, 3)

        self.third_row.addWidget(self.radio_end_fk_control)

        self.fourth_row.addWidget(self.btn_color_ik)
        self.fourth_row.addWidget(self.btn_color_fk)

        self.radio_end_fk_control.setChecked(True)

        self.ver_layout.addLayout(self.choice_row)
        self.ver_layout.addLayout(self.first_row)
        self.ver_layout.addLayout(self.sec_row)
        self.ver_layout.addLayout(self.third_row)
        self.ver_layout.addLayout(self.fourth_row)
        self.ver_layout.addWidget(self.btn_create_system)

        self.btn_parent_joint.clicked.connect(self.add_parent_joint)
        self.btn_end_joint.clicked.connect(self.add_end_joint)

        self.btn_color_ik.clicked.connect(partial(self.choose_color, self.btn_color_ik))
        self.btn_color_fk.clicked.connect(partial(self.choose_color, self.btn_color_fk))

        self.cmb_control_type.currentTextChanged.connect(self.check_fk)

        self.btn_create_system.clicked.connect(self.create_system)

    def add_parent_joint(self):
        self.txt_parent_joint.setText(cmds.ls(sl=True)[0])

    def add_end_joint(self):
        self.txt_end_joint.setText(cmds.ls(sl=True)[0])

    def create_system(self):
        control = IkFkSwitch(self.txt_parent_joint.text(), self.txt_end_joint.text())
        colors = {'ik': self.ik_color, 'fk': self.fk_color}
        if self.cmb_control_type.currentText() == 'IK / FK':
            control.build(0, 'include', colors) if self.radio_end_fk_control.isChecked() else control.build(0,
                                                                                                            'exclude',
                                                                                                            colors)
        elif self.cmb_control_type.currentText() == 'FK only':
            control.build(1, 'include', colors) if self.radio_end_fk_control.isChecked() else control.build(1,
                                                                                                            'exclude',
                                                                                                            colors)
        else:
            control.build(2, 'include', colors)

    def check_fk(self):
        if self.cmb_control_type.currentIndex() == 1:
            self.radio_end_fk_control.setDisabled(True)
        else:
            self.radio_end_fk_control.setDisabled(False)

    def choose_color(self, button):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet("QPushButton {background-color:" + color.name() + "; color: white;}")
        if button.text() == 'IK':
            self.ik_color = self.to_rgb(color.rgb())
        if button.text() == 'FK':
            self.fk_color = self.to_rgb(color.rgb())

    @staticmethod
    def to_rgb(int_value):
        red = ((int_value >> 16) & 255) / 255
        blue = (int_value & 255) / 255
        green = ((int_value >> 8) & 255) / 255
        return red, green, blue


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
