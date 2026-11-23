# -*- coding: utf-8 -*-
"""第 1 阶段人工译文表（材质/资源 术语规范）。"""

STAGE1_ZH = {
    # ---- 格式与专名：保持原样 ----
    '3DS': '3DS',
    'DXF': 'DXF',
    'c2fc': 'c2fc',
    'HexaSuper': 'HexaSuper',
    'LightWave3D': 'LightWave3D',
    'WavefrontObj': 'WavefrontObj',
    'CLIP STUDIO MODELER': 'CLIP STUDIO MODELER',
    '8 bit': '8 位',
    '16 bit': '16 位',
    '8.000 kHz': '8.000 kHz',
    '11.025 kHz': '11.025 kHz',
    '22.050 kHz': '22.050 kHz',
    '44.100 kHz': '44.100 kHz',

    # ---- 窗口排列 ----
    'Tiled': '平铺',
    'Cascade': '层叠',

    # ---- 界面部件 ----
    'Command': '命令',
    'Command bar': '命令栏',
    'Status bar': '状态栏',
    'Show all': '显示全部',
    'Show all palettes': '显示所有面板',
    'Recent': '最近',

    # ---- 节点/网格 ----
    'Mesh tree': '网格树',
    'Root node': '根节点',
    'Delete node': '删除节点',
    'Duplicate node': '创建节点副本',
    'Mesh information': '网格信息',
    'Manipulator': '操作手柄',

    # ---- 新建 ----
    'New shape': '新建形状',
    'New object ': '新建对象',
    'New material': '新建材质',
    'New character': '新建角色',
    'New background': '新建背景',
    'Type of work': '作品类型',
    '3D background': '3D 背景',

    # ---- 动作与设置 ----
    'Play motion': '播放动作',
    'View settings': '视图设置',
    'Camera settings': '摄像机设置',
    'Skirt settings': '裙摆设置',
    'Physics settings': '物理设置',
    'Physical object': '物理对象',
    'Bone configuration': '骨骼配置',
    'Bone information': '骨骼信息',
    'Character configuration': '角色配置',
    'Character information': '角色信息',
    'Quad screen view': '四视图',
    'Single screen view': '单视图',
    'Surface material': '表面材质',
    'Surface material attribute': '表面材质属性',
    'Merge same materials': '合并相同材质',

    # ---- 许可证 ----
    'Check License': '检查许可证',
    'Register License': '注册许可证',
    'Use all functions free of charge.': '所有功能均可免费使用。',
    'To save any 3D shapes created within the project, it is necessary to register a license.':
        '要保存项目中创建的 3D 形状，需要注册许可证。',
    'If you have a serial number for Clip Studio Modeler, please press the [Register license] button.':
        '如果您有 CLIP STUDIO MODELER 的序列号，请点击[注册许可证]按钮。',
    'If you have a serial number for Clip Studio Modeler, \r\nplease press the [Register license] button.':
        '如果您有 CLIP STUDIO MODELER 的序列号，\r\n请点击[注册许可证]按钮。',

    # ---- 导入导出 ----
    'Export 3DS format': '导出 3DS 格式',
    'Export DXF format': '导出 DXF 格式',
    'Export HexaSuper format': '导出 HexaSuper 格式',
    'Export LightWave3D format': '导出 LightWave3D 格式',
    'Export WavefrontObj format': '导出 WavefrontObj 格式',
    'Import DXF format': '导入 DXF 格式',
    'Import LightWave3D format': '导入 LightWave3D 格式',
    'Import WavefrontObj format': '导入 WavefrontObj 格式',

    # ---- 视角 ----
    'Undo point of view': '撤销视角操作',
    'Redo point of view': '重做视角操作',
    'View entire object': '显示整个对象',
    'Return to default viewing angle': '恢复默认视角',
    'Reset to default': '恢复默认值',
    'Use selected area as the center of display rotation': '以选中区域作为显示旋转中心',
    'Quad screen view': '四视图',

    # ---- 显示/隐藏 ----
    'Hide selected area': '隐藏选中区域',
    'Hide only vertices and edges': '仅隐藏顶点和边',
    'Hide everything except selected area': '隐藏选中区域以外的内容',
    'Hide everything outside of selected area': '隐藏选中区域之外的内容',
    'Hide symmetric projection': '隐藏对称投影',
    'Culling (Front-face)': '剔除（正面）',
    'Culling (Back-face)': '剔除（背面）',

    # ---- 角度/布局 ----
    'Save 3D object angle': '保存 3D 对象角度',
    'Save 3D object layout ': '保存 3D 对象布局',
    'Apply angle to 3D object': '将角度应用到 3D 对象',
    'Apply layout to 3D object': '将布局应用到 3D 对象',

    # ---- 状态提示 ----
    'Adjusting origin position...': '正在调整原点位置...',
    'Recalculating normals...': '正在重新计算法线...',
    'Graphics performance check': '图形性能检查',
    'Current file format cannot be edited.': '当前文件格式无法编辑。',

    # ---- 帮助菜单 ----
    'Instruction Manual': '使用手册',
    'Training and Tutorials': '培训与教程',
    'CLIP website': 'CLIP 官网',
    'CLIP STUDIO MODELER Manual': 'CLIP STUDIO MODELER 手册',
    'CLIP STUDIO MODELER Support': 'CLIP STUDIO MODELER 支持',
    'CLIP STUDIO MODELER Training and Tutorials': 'CLIP STUDIO MODELER 培训与教程',

    # ---- 对话框 ----
    'Show this dialogue when starting CLIP STUDIO MODELER': '启动 CLIP STUDIO MODELER 时显示此对话框',

    # ---- 错误提示 ----
    'Cannot open file as COORDINATE license has been registered':
        '已注册 COORDINATE 许可证，无法打开此文件。',
    'Failed to load file. Cannot open character format CMO file.':
        '文件加载失败。无法打开 CMO 角色格式文件。',
    'Unable to save in current format because the mesh does not exist.':
        '网格不存在，无法以当前格式保存。',
    'Unable to save in current format because the model has not been loaded.':
        '模型尚未加载，无法以当前格式保存。',
    'Unable to save in current format as movability is set without a key frame.':
        '在未设置关键帧的情况下设置了可动性，无法以当前格式保存。',
    'Restricted functionality does not allow for data created in this format be saved.':
        '受限功能不允许保存以该格式创建的数据。',

    # ---- 文件类型过滤器 ----
    'CLIP STUDIO MODELER File (*.cmo)|*.cmo|CELSYS CHARACTER format (*.c2fc)|*.c2fc':
        'CLIP STUDIO MODELER 文件 (*.cmo)|*.cmo|CELSYS 角色格式 (*.c2fc)|*.c2fc',

    # ---- 长说明 ----
    'Load 3D data to set up [3D Character] for use in Clip Studio Paint.\r\nSet up bones within the 3D data usable for Clip Studio Paint to arrange poses freely.':
        '加载 3D 数据，将其设置为可在 Clip Studio Paint 中使用的[3D 角色]。\r\n为 3D 数据设置骨骼，即可在 Clip Studio Paint 中自由摆姿势。',
    'Create new [3D Shape]. \r\nCreate new shapes from scratch by polygon modelling via simple operations\r\n and use as 3D object, 3D background or as parts of other 3D data.':
        '新建 [3D 形状]。\r\n通过简单的多边形建模操作从零创建新形状，\r\n可用作 3D 对象、3D 背景，或其他 3D 数据的部件。',
    'Load 3D data to set up [3D Object] for use in Clip Studio Paint. \r\nSettings for exchanging numerous textures or movability settings for moving special parts via a slider can be added.\r\nBy adding these settings, Clip Studio Paint allows the [3D Object] display to be customized.':
        '加载 3D 数据，将其设置为可在 Clip Studio Paint 中使用的[3D 对象]。\r\n可添加纹理替换设置，或通过滑块移动特殊部件的可动性设置。\r\n添加这些设置后，Clip Studio Paint 便可自定义 [3D 对象]的显示方式。',
}

if __name__ == '__main__':
    print(f'第 1 阶段译文 {len(STAGE1_ZH)} 条')
