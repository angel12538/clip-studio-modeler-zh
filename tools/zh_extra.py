# -*- coding: utf-8 -*-
"""补充词表：模板串与长段落断行修正。

这些条目在早期是单独用补丁脚本处理的，现在整合进一键流程。
"""

ZH_EXTRA = {
    # ---- 模板串（%s 位置按中文语序调整）----
    'Create %s': '创建%s',

    # ---- 新建对话框说明（按控件宽度手动断行）----
    'Load 3D data to set up [3D Object] for use in Clip Studio Paint. \r\n'
    'Settings for exchanging numerous textures or movability settings for moving special parts via a slider can be added.\r\n'
    'By adding these settings, Clip Studio Paint allows the [3D Object] display to be customized.':
        '加载 3D 数据，设为可在 Clip Studio Paint 中使用的[3D 对象]。\r\n'
        '可添加纹理替换、特殊部件可动性等设置。',

    'Load 3D data to set up [3D Character] for use in Clip Studio Paint.\r\n'
    'Set up bones within the 3D data usable for Clip Studio Paint to arrange poses freely.':
        '加载 3D 数据，设为可在 Clip Studio Paint 中使用的[3D 角色]。\r\n'
        '为 3D 数据设置骨骼，即可自由摆姿势。',

    'Create new [3D Shape]. \r\n'
    'Create new shapes from scratch by polygon modelling via simple operations\r\n'
    ' and use as 3D object, 3D background or as parts of other 3D data.':
        '新建 [3D 形状]，通过多边形建模从零创建新形状，\r\n'
        '可用作 3D 对象、3D 背景或其他 3D 数据的部件。',

    'Load 3D data to set up [3D Background] for use in Clip Studio Paint. \r\n'
    'When setting up the camera angle for displaying the background, these angles can be selected in Clip Studio Paint. \r\n'
    'Exchangeable textures and parts can be set, as well as special parts that can be moved via a slider can be added within the movability settings.':
        '加载 3D 数据，设为可在 Clip Studio Paint 中使用的[3D 背景]。\r\n'
        '可设置背景显示用的摄像机角度，并可在 Clip Studio Paint 中选择。\r\n'
        '可设置可替换的纹理与部件，也可添加通过滑块移动的特殊部件。',
}

if __name__ == '__main__':
    print('补充词表 %d 条' % len(ZH_EXTRA))
    for k in ZH_EXTRA:
        print('  %r' % k[:60])
