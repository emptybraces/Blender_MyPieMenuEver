import bpy
from bpy.types import Panel, Menu, Operator
from . import _Util

# --------------------------------------------------------------------------------
# ポーズメニュー
# --------------------------------------------------------------------------------
def MenuPrimary(pie, context):
    arm = bpy.context.object.data;
    box = pie.split().box()
    box.label(text = 'Pose')
    col = box.column()

    col.operator(OT_ClearTransform.bl_idname)
    col.row().prop(arm, "pose_position", expand=True)
    col.prop(arm, 'layers')

class OT_ClearTransform(bpy.types.Operator):
    bl_idname = "op.clear_transform"
    bl_label = "Clear Transform"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        selected_objects = context.selected_objects
        for obj in selected_objects:
            _Util.reset_pose_bone(obj)
        # 古い処理
        # current_mode = context.active_object.mode
        # # backup
        # buf = []
        # for i in range(32):
        #     buf.append(bpy.context.object.data.layers[i])
        #     bpy.context.object.data.layers[i] = True
        # # execution
        # bpy.ops.pose.select_all(action='SELECT')
        # bpy.ops.pose.rot_clear()
        # bpy.ops.pose.loc_clear()
        # bpy.ops.pose.scale_clear()
        # # restore
        # for i in range(32):
        #     bpy.context.object.data.layers[i] = buf[i]
        # bpy.ops.object.mode_set( mode = current_mode)
        return {'FINISHED'}
# --------------------------------------------------------------------------------
def MenuSecondary(pie, context):
    pass


# --------------------------------------------------------------------------------
classes = (
    OT_ClearTransform,
)
def register():
    _Util.register_classes(classes)
def unregister():
    _Util.unregister_classes(classes)