# -*- coding: utf-8 -*-
"""批次 6：长提示语与剩余界面文本（终批）。"""

ZH_BATCH6 = {
    # ---- 建模错误提示 ----
    'Cannot be processed because there are no meshes, or meshes are stored in different folders.':
        '无法处理：没有网格，或网格存放在不同文件夹中。',
    'Cannot change selection of main view while mesh element is selected.':
        '选中网格元素时无法更改主视图的选择。',
    'Cannot create pipe mesh if cross-section mesh or trajectory mesh contains faces, or if trajectory is branched or closed in a circle.':
        '截面网格或轨迹网格包含面，或轨迹有分支/闭合成环时，无法创建管状网格。',
    'Cannot execute Boolean operation or subtraction because the shape is too complex (shapes are intersecting).':
        '形状过于复杂（形状相互交叉），无法执行布尔运算或差集。',
    'Cannot execute Boolean operation, subtraction, or division into circles and rectangles because the shape is too complex.':
        '形状过于复杂，无法执行布尔运算、差集，或按圆形/矩形分割。',
    'Cannot execute operation. Meshes from default folders and symmetric folders can not be merged or grouped. \r\n(Please use operation after converting symmetry folder to default folder via the mesh tree panel.)':
        '无法执行操作。默认文件夹与对称文件夹中的网格不能合并或分组。\r\n（请先在网格树面板中将对称文件夹转换为默认文件夹，再执行操作。）',
    'Cannot execute process as current folder has been set to invisible or editing is turned off.':
        '当前文件夹已设为不可见或编辑已关闭，无法执行此操作。',
    'Cannot execute process due to an error. (Function not implemented)':
        '因错误无法执行此操作。（功能未实现）',
    'Cannot execute process due to lack of memory. Please close unnecessary documents, other applications or Modeler to increase the allocated memory.':
        '内存不足，无法执行此操作。请关闭不必要的文档、其他应用程序或 Modeler 以增加可用内存。',
    'Cannot open file. This file is for dedicated use with Sashi-E Studio for CLIP. Open the file in Sashi-E Studio for CLIP and save the file again from the menu as [File / HexaSuper format] to open again.':
        '无法打开文件。此文件专供 Sashi-E Studio for CLIP 使用。请在 Sashi-E Studio for CLIP 中打开该文件，从菜单以[文件 / HexaSuper 格式]重新保存后再打开。',
    'Cannot register material, as face holding mesh does not exist.': '不存在承载脸部的网格，无法注册材质。',
    'Cannot save in the specified folder. Please choose another location to save the material.':
        '无法保存到指定文件夹。请选择其他位置保存材质。',
    'Cannot set target folder of current edited mesh to become invisible.': '无法将当前编辑网格的目标文件夹设为不可见。',
    'Cannot turn off editing for target folder of current edited mesh.': '无法关闭当前编辑网格目标文件夹的编辑。',
    'Cannot undo operations from mesh tree. Are you sure you want to continue?': '无法撤销来自网格树的操作。确定要继续吗？',
    'Could not execute Boolean operation or subtraction because the intersecting parts are disconnected.':
        '相交部分不连续，无法执行布尔运算或差集。',
    'Element selected instead of mesh. Do you wish to invert all faces connected to the element?':
        '选中的是元素而非网格。要反转与该元素连接的所有面吗？',
    'Executing Boolean operation between the two chosen meshes. Results can vary with regards to the reverse side of the faces of the meshes.':
        '正在对选中的两个网格执行布尔运算。结果可能因网格面的反面而有所不同。',
    'Curved mesh not selected. Please select a mesh that the [Curve surface] command has been applied to.':
        '未选择曲面网格。请选择已应用[曲面]命令的网格。',
    'Mesh not selected. Please select angle of selection frame for the mesh to be reset. ':
        '未选择网格。请选择要重置的选择框角度。',
    'Mesh not selected. Please select outline of solid revolution for the wireframe mesh.':
        '未选择网格。请为线框网格选择实体旋转的外形轮廓。',
    'Mesh or element has not been copied and cannot be pasted. Please copy a mesh or element to paste.':
        '未复制网格或元素，无法粘贴。请先复制要粘贴的网格或元素。',
    'No mesh or element selected. Please select mesh or element to configure mesh as center of rotation.':
        '未选择网格或元素。请选择要设为旋转中心的网格或元素。',
    'No mesh or element selected. Please select mesh to or edge element to create sharp edge.':
        '未选择网格或元素。请选择网格或边元素以创建锐边。',
    'No mesh or element selected. Please select mesh to or edge element to remove sharp edge.':
        '未选择网格或元素。请选择网格或边元素以移除锐边。',
    'No mesh or element selected. Please select mesh wireframe or element to add face.':
        '未选择网格或元素。请选择网格线框或元素以添加面。',

    # ---- 图形性能 ----
    'Check the graphics performance in the using environment and whether 3D features of the software\r\nwill work correctly. Proceed to graphics performance check?':
        '检查当前环境下的图形性能，以及软件的 3D 功能能否正常工作。\r\n是否进行图形性能检查？',
    "If 3D function doesn't work correctly when using it, click \r\n the below button and check the operation environment.":
        '如果使用 3D 功能时工作不正常，请点击\r\n下方按钮检查运行环境。',
    "If 3D function doesn't work correctly when using it, it may be fixed with \r\n the update of graphic driver.":
        '如果使用 3D 功能时工作不正常，更新显卡驱动可能可以解决。',
    'If the software does not start correctly or works slowly, click \r\n the below button and check the operation environment.':
        '如果软件无法正常启动或运行缓慢，请点击\r\n下方按钮检查运行环境。',
    'If the software does not start correctly or works slowly, it may be fixed with \r\n the update of graphic driver.':
        '如果软件无法正常启动或运行缓慢，更新显卡驱动可能可以解决。',
    'If you want to use 3D function, please check \r\n the operation environment for 3D function from the below web page and use the appropriate computer.':
        '如需使用 3D 功能，请从下方网页检查\r\n 3D 功能的运行环境，并使用合适的计算机。',

    # ---- 确认对话框 ----
    'If you perform this operation, the created standard feature point will become non-standard. Proceed?':
        '执行此操作后，已创建的标准特征点将变为非标准。继续吗？',
    'If you perform this operation, you will no longer be able to adjust the position, direction, and scale. Proceed?':
        '执行此操作后，将无法再调整位置、方向和比例。继续吗？',
    'If you perform this operation, you will no longer be able to make adjustments to the paste texture. Proceed?':
        '执行此操作后，将无法再调整粘贴的纹理。继续吗？',
    'If you perform this operation, you will not be able to undo actions made before this point. Proceed?':
        '执行此操作后，将无法撤销此前所做的操作。继续吗？',
    'Facial expression texture information will be discarded.\r\nYou will not be able to undo actions made before this point. Proceed?':
        '表情纹理信息将被丢弃。\r\n将无法撤销此前所做的操作。继续吗？',
    'Pasted texture information will be discarded.\r\nYou will not be able to undo actions made before this point. Proceed?':
        '已粘贴的纹理信息将被丢弃。\r\n将无法撤销此前所做的操作。继续吗？',
    'Do you want to replace the existing default settings and save the current settings as default for the selected sub tool?':
        '要替换现有的默认设置，并将当前设置保存为选中辅助工具的默认值吗？',

    # ---- 试用期到期 ----
    'Clip Studio Modeler version 1.6.0 has expired.\r\nThank you for using Clip Studio Modeler.\r\n\r\nWe are developing several services for your creative activities in Clip Studio.\r\n\r\n[Creative Activity Support "CLIP" ]':
        'CLIP STUDIO MODELER 1.6.0 版本已到期。\r\n感谢您使用 CLIP STUDIO MODELER。\r\n\r\n我们正在为您在 CLIP STUDIO 中的创作活动开发多项服务。\r\n\r\n[创作活动支持 "CLIP"]',

    # ---- 3D 背景说明 ----
    'Load 3D data to set up [3D Background] for use in Clip Studio Paint. \r\nWhen setting up the camera angle for displaying the background, these angles can be selected in Clip Studio Paint. \r\nExchangeable textures and parts can be set, as well as special parts that can be moved via a slider can be added within the movability settings.':
        '加载 3D 数据，将其设置为可在 Clip Studio Paint 中使用的[3D 背景]。\r\n为背景设置显示用摄像机角度后，可在 Clip Studio Paint 中选择这些角度。\r\n可设置可替换的纹理与部件，并可在可动性设置中添加通过滑块移动的特殊部件。',

    # ---- 拖拽提示 ----
    'Left drag: Change angle  Middle drag: Move vertically/horizontally  Right drag: Move back and forth':
        '左键拖拽：改变角度  中键拖拽：垂直/水平移动  右键拖拽：前后移动',
    'Left drag: Change angle    Middle drag: Move vertically/horizontally    Control: Move back and forth':
        '左键拖拽：改变角度    中键拖拽：垂直/水平移动    Control：前后移动',

    # ---- 图案 ----
    'Color pattern:Effect and feeling:Bright, Quiet, Soft and Delight': '彩色图案：效果与情绪：明亮、安静、柔和、愉悦',
    'Monochromatic pattern:Effect and feeling:Bright, Quiet, Soft and Delight': '单色图案：效果与情绪：明亮、安静、柔和、愉悦',

    # ---- 文件夹重复提示 ----
    'A “%s” folder already exists, so the file was downloaded to a new folder called “%s”.':
        '名为“%s”的文件夹已存在，因此文件已下载到名为“%s”的新文件夹中。',
    'A “%s” folder already exists, so the file was moved to a new folder called “%s”.':
        '名为“%s”的文件夹已存在，因此文件已移动到名为“%s”的新文件夹中。',

    # ---- 3D 分类补漏（日文键对应的英文名）----
    '3D:Background': '3D：背景',
    '3D:Character': '3D：角色',
    '3D:Character Texture': '3D：角色纹理',
    '3D:Character Texture:Face': '3D：角色纹理：脸部',
    '3D:Character parts': '3D：角色部件',
    '3D:Motion': '3D：动作',
    '3D:Pose': '3D：姿势',
    '3D:Pose:Hand': '3D：姿势：手部',
    'Download:Material': '下载：材质',

    # ---- 中文键（CELSYS 原生日文残留，一并本地化）----
    '3D:キャラクター': '3D：角色',
    '3D:キャラクターテクスチャ': '3D：角色纹理',
    '3D:キャラクターテクスチャ:フェイス': '3D：角色纹理：脸部',
    '3D:キャラクターパーツ': '3D：角色部件',
    '3D:キャラクターパーツ:フェイス': '3D：角色部件：脸部',
    '3D:キャラクターパーツ:ヘア': '3D：角色部件：头发',
    '3D:キャラクターパーツ:ボディ': '3D：角色部件：身体',
    '3D:ポーズ': '3D：姿势',
    '3D:モーション': '3D：动作',
    '3D:モーション:カメラ': '3D：动作：摄像机',
    '3D:モーション:キャラクター': '3D：动作：角色',
    '3Dデータコレクション': '3D 数据合集',
    'CLIPマテリアル': 'CLIP 材质',
}
