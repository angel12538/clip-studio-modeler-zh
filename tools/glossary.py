# -*- coding: utf-8 -*-
"""术语表：按用户要求（材质/资源）统一，并修正官方词典里的旧术语。"""

# 英文 -> 简体中文（权威定名，翻译时优先查这张表）
TERMS = {
    # ---- 3D 核心术语 ----
    'Material': '材质',
    'Materials': '材质',
    'Texture': '纹理',
    'Textures': '纹理',
    'Asset': '资源',
    'Assets': '资源',
    'Resource': '资源',
    'Resources': '资源',

    # ---- 3D 对象与部件 ----
    'Object': '对象',
    'Objects': '对象',
    '3D Object': '3D 对象',
    '3D Folder': '3D 文件夹',
    'Node': '节点',
    'Mesh': '网格',
    'Polygon': '多边形',
    'Vertex': '顶点',
    'Vertices': '顶点',
    'Edge': '边',
    'Edges': '边',
    'Face': '面',
    'Faces': '面',

    # ---- 角色与骨骼 ----
    'Character': '角色',
    'Bone': '骨骼',
    'Bones': '骨骼',
    'Joint': '关节',
    'Pose': '姿势',
    'Body': '身体',
    'Head': '头部',
    'Hair': '头发',
    'Accessories': '配饰',
    'Facial expression': '表情',
    'Facial expression parts': '表情部件',

    # ---- 场景 ----
    'Scene': '场景',
    'Camera': '摄像机',
    'Light': '光照',
    'Lighting': '光照',
    'Ambient light': '环境光',
    'Parallel light': '平行光',
    'Point light': '点光源',
    'Shadow': '阴影',
    'Shadows': '阴影',

    # ---- 视图 ----
    'View': '视图',
    'Perspective': '透视',
    'Orthographic': '正交',
    'Wireframe': '线框',
    'Outline': '轮廓',
    'Culling': '剔除',
    'No culling': '不剔除',

    # ---- 文件操作 ----
    'File': '文件',
    'New': '新建',
    'Open': '打开',
    'Close': '关闭',
    'Save': '保存',
    'Save as': '另存为',
    'Export': '导出',
    'Import': '导入',
    'Undo': '撤销',
    'Redo': '重做',
    'Cut': '剪切',
    'Copy': '复制',
    'Paste': '粘贴',
    'Delete': '删除',
    'Clear': '清除',
    'Duplicate': '创建副本',
    'Select all': '全选',
    'Deselect': '取消选择',
    'Invert selection': '反选',

    # ---- 界面 ----
    'Window': '窗口',
    'Workspace': '工作区',
    'Tool': '工具',
    'Tools': '工具',
    'Sub tool': '辅助工具',
    'Tool properties': '工具属性',
    'Object information': '对象信息',
    'Object configuration': '对象配置',
    'Navigator': '导航器',
    'Layer': '图层',
    'Layers': '图层',
    'Property': '属性',
    'Properties': '属性',
    'Setting': '设置',
    'Settings': '设置',
    'Option': '选项',
    'Options': '选项',
    'Preview': '预览',
    'Display': '显示',
    'Show': '显示',
    'Hide': '隐藏',
    'Edit': '编辑',
    'Help': '帮助',
    'Version': '版本',
    'Version information': '版本信息',
    'Customize': '自定义',
    'Quit': '退出',
    'Cancel': '取消',
    'OK': '确定',
    'Apply': '应用',
    'Reset': '重置',
    'Default': '默认',
    'Name': '名称',
    'Comment': '备注',
    'Size': '尺寸',
    'Angle': '角度',
    'Layout': '布局',
    'Sketch': '草图',
    'Allocate': '分配',
    'Movable parts': '可动部件',
    'Unique point': '特征点',
    'Character Motion': '角色动作',
    'Recent file': '最近文件',
    'None': '无',
    'Document': '文档',
    'New window': '新建窗口',
    'Start CLIP STUDIO': '启动 CLIP STUDIO',
    'Register material': '注册材质',
    'Register as new material': '注册为新材质',
    'Save material and close program': '保存材质并关闭程序',
    'About CLIP STUDIO MODELER': '关于 CLIP STUDIO MODELER',
    'Quit CLIP STUDIO MODELER': '退出 CLIP STUDIO MODELER',
    'CLIP STUDIO 3D File': 'CLIP STUDIO 3D 文件',
}

# 遗留术语修正：官方繁中里这些词要按新规范替换
LEGACY_FIX = [
    ('素材', '材质'),      # 仅在上下文明确定为 Material 时替换
    ('材質', '材质'),      # 繁->简
    ('檔案', '文件'),
    ('檢視', '视图'),
    ('視窗', '窗口'),
    ('說明', '帮助'),
]

if __name__ == '__main__':
    print(f'术语表 {len(TERMS)} 条')
    for k, v in list(TERMS.items())[:20]:
        print(f'  {k:<28} -> {v}')
