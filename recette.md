STEPS TO CREATE IK FK SYSTEM

1. Create a joint chain
![img_1.png](img_1.png)

2. Orient the axis of the joint chain in the correct direction with respect to the rotation order
![img_2.png](img_2.png)

3. Rename the joint chain correctly eg: joint_JNT \
![img_3.png](img_3.png)

4. Duplicate the joint chain twice and rename the first joint chain by adding a suffix IK
![img_4.png](img_4.png)

5. Rename the second joint chain by adding a suffix FK \
![img_5.png](img_5.png)

6. Following the joints in the caption, select arm_IK_JNT, arm_FK_JNT then arm_JNT
respectfully, apply a parent_constraint
![img_6.png](img_6.png)

7. Repeat step 6 for forearm_IK_JNT, forearm_FK_JNT forearm_JNT
and wrist_IK_JNT, wrist_FK_JNT, wrist_JNT.
You should have your constraints create on the main joint chain
![img_9.png](img_9.png)
8. the constraint has the weighting of the 2 joints IK and FK
![img_7.png](img_7.png)
![img_10.png](img_10.png)

9. FK Control rig creation
Create a curve to represent the FK control rig
Create a nurbs circle curve for each joint on the FK joint chain respectively:
control rig | joint
arm_FK_CTRL    | arm_FK_JNT
forearm_FK_CTRL| forearm_FK_JNT
wrist_FK_CTRL  | wrist__FK_JNT

10. Control rig workflow
To have a control rig that functions properly, the orientations of the nurbs
curve has to match the orientation of the joint it is going to control, to achieve this we
need to:
 - Choose the initial orientation you want for the nurbs curve
 - Select the nurbs curve then the joint and press P to parent the curve to the joint,
 - ![img_12.png](img_12.png)
 - Freeze the transform of the control curve, this will give the transform of the joints 
to the control curve
 - unparent the control curve from the joint
 - Select the control curve then joint and apply a parent constraint 
wih the following settings for the parent constraint
 - ![img_11.png](img_11.png)

Control rig organization 
We need to arrange the control curve properly in the outliner, but before 
doing so the transforms has to be neutralized to zero.
- create an empty group and give it the name of the joint with the suffix "offset"
![img_13.png](img_13.png)
- parent this new group to the control curve 
- change the transform of the pivot of the group to match the control curve
- and apply a freeze transform 
- unparent the group from the control curve and parent the control curve to the group
- this should set the transforms of the control curve to 0.

![img_14.png](img_14.png)

12. IK Control rig creation
13. Create an ik handle with rotate plane solver by selecting arm_IK_JNT and wrist_IK_JNT
![img_15.png](img_15.png)
14. Create a curve to represent the IK control rig
15. 
16. select the Ik control curve then the ik handle and apply a point constraint

Creating the IK FK Blend
1. select the control curve that will have the attribute
![img_16.png](img_16.png)
![img_17.png](img_17.png)
