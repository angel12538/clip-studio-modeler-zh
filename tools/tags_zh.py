# -*- coding: utf-8 -*-
"""素材标签与文件夹标签的翻译表。"""

# ---- 用户标签（Tag 表 / info.xml）----
TAG_ZH = {
    'Male': '男性',
    'Female': '女性',
    'Character_Texture': '角色纹理',
    'Eyes': '眼睛',
    'Mouth': '嘴',
    'Whole_Face': '整张脸',
    'Basic': '基础',
    'Petite': '娇小',
    'Hourglass': '沙漏型',
    'Muscular': '肌肉型',
}

# ---- 系统标签（SystemTag 表）----
# 这些是程序内部键，留在库里做匹配；界面显示另由资源文件映射决定。
SYSTEMTAG_ZH = {
    'CharacterPartsBody': '角色部件：身体',
    'CharacterPartsFace': '角色部件：脸部',
    'CharacterPartsHair': '角色部件：头发',
    'Resizable': '可调整尺寸',
}

# ---- 文件夹标签（FolderTag 表）---- 
# 原库是日文，需要转中文；同时资源文件里也有同名键，两处应当一致。
FOLDERTAG_ZH = {
    '3D:キャラクターパーツ:ボディ': '3D：角色部件：身体',
    '3D:キャラクターパーツ:フェイス': '3D：角色部件：脸部',
    '3D:キャラクターパーツ:ヘア': '3D：角色部件：头发',
    '3D:キャラクターテクスチャ:フェイス': '3D：角色纹理：脸部',
}

if __name__ == '__main__':
    print(f'用户标签 {len(TAG_ZH)} 条')
    print(f'系统标签 {len(SYSTEMTAG_ZH)} 条')
    print(f'文件夹标签 {len(FOLDERTAG_ZH)} 条')
