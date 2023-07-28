import bpy
from mathutils import Vector, Quaternion
from bpy.types import Panel, Menu, Operator
from rna_prop_ui import PropertyPanel
from bpy.app.translations import (
    pgettext_iface as iface_,
    pgettext_tip as tip_,
    contexts as i18n_contexts,
)
# HT – ヘッダー
# MT – メニュー
# OT – オペレーター
# PT – パネル
# UL – UIリスト
class OT_InvertValue(bpy.types.Operator):
    bl_idname = "op.invert_value"
    bl_label = ""
    propName: bpy.props.StringProperty()
    def execute(self, context):
        target = getattr(context, self.propName, None)
        setattr(target, self.propName, not getattr(target, self.propName))
        return {'FINISHED'}
    @staticmethod
    def operator(layout, label, propName, targetObj, isActive = True, ctxt = ''):
        layout.context_pointer_set(name=propName, data=targetObj)
        op = layout.operator(OT_InvertValue.bl_idname, text=label, text_ctxt =ctxt, depress=layout.active and getattr(targetObj, propName, False))
        op.propName = propName
        layout.enabled = isActive and targetObj != None
class OT_SetValue(bpy.types.Operator):
    bl_idname = "op.valueset"
    bl_label = ""
    propName: bpy.props.StringProperty()
    value: bpy.props.FloatProperty()
    def execute(self, context):
        target = getattr(context, self.propName, None)
        setattr(target, self.propName, self.value)
        return {'FINISHED'}
    @staticmethod
    def operator(layout, label, targetObj, propName, value, isActive = True, ctxt = ''):
        layout.context_pointer_set(name=propName, data=targetObj)
        op = layout.operator(OT_SetValue.bl_idname, text=label, text_ctxt =ctxt)
        op.propName = propName
        op.value = value
        layout.enabled = isActive and targetObj != None

# --------------------------------------------------------------------------------
def show_enum_values(obj, prop_name):
    print([item.identifier for item in obj.bl_rna.properties[prop_name].enum_items])
def enum_values(obj, prop_name):
    return [item.identifier for item in obj.bl_rna.properties[prop_name].enum_items]
def layout_prop_noneable(layout, target, prop, text=None, expand=False):
    if target != None:
        layout.prop(target, prop, text=text, expand=expand)
    else:
        layout.label(text='None')
def layout_operator(layout, opid, label=None, isActive=None):
    if isActive == None:
        return layout.operator(opid, text=label)
    else:
        r = layout.row()
        r.active = isActive
        return r.operator(opid, text=label)
def reset_pose_bone_location(armature):
    if armature.type == 'ARMATURE':
        for b in armature.pose.bones:
            b.location = Vector((0, 0, 0))
def reset_pose_bone_rotation(armature):
    if armature.type == 'ARMATURE':
        for b in armature.pose.bones:
            b.rotation_euler = (0, 0, 0)
def reset_pose_bone_scale(armature):
    if armature.type == 'ARMATURE':
        for b in armature.pose.bones:
            b.scale = Vector((1, 1, 1))
def reset_pose_bone(armature):
    reset_pose_bone_location(armature)
    reset_pose_bone_rotation(armature)
    reset_pose_bone_scale(armature)
def register_classes(classes):
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            print(e)
def unregister_classes(classes):
    for cls in classes:
        bpy.utils.unregister_class(cls)
def is_armature_in_selected():
    for obj in bpy.context.selected_objects:
        if obj.type == 'ARMATURE':
            return True
    return False
def show_msgbox(message, title = "", icon = 'INFO'):
    def draw(self, context):
        lines = message.split('\n')
        for line in lines:
            self.layout.label(text=line)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
def get_prefs():
    print(__name__)
    return bpy.context.preferences.addons["my_pie_menu_ever"].preferences
# --------------------------------------------------------------------------------
classes = (
    OT_InvertValue,
    OT_SetValue,
)
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
