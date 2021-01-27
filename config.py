import json
anonym = {}
# synonym = {}

characters = [
    '上', '下', '左', '右', '前', '后', '进', '出', '来', '去', '东', '南', '西', '北', '里', '外'
    # '回', '过', '起', 
]

class generalModel(object):
    roots = []
    prefixes = []
    suffixes = [
        '边', '部', '方', '面', '头', '端', '侧',
    ]

    def __init__(self, pos):
        self.framework = {}
        self.pos = pos

    def generateFramework(self):
        for root in self.roots:
            self.framework[root] = ''

    # 前缀派生
    @classmethod
    def prefixDerivate(cls):
        return [ [ prefix + r for prefix in cls.prefixes ] for root in cls.roots for r in root]

    # 后缀派生
    @classmethod
    def suffixDerivate(cls):
        return [ [ r + suffix for suffix in cls.suffixes ] for root in cls.roots for r in root]

    # 普通后缀派生
    @classmethod
    def generalSuffixDerivate(cls):
        return [ [ r + suffix for suffix in generalModel.suffixes ] for root in cls.roots for r in root]

    # 指定root的所有派生
    @classmethod
    def general(cls, root):
        return [ root + suffix for suffix in generalModel.suffixes ] + [ root + suffix for suffix in cls.suffixes ] + [ prefixes + root for prefixes in cls.prefixes ]
    

# 方位指示代词
class indicationWords(generalModel):
    roots = [
        ['这'], ['那'], 
    ]
    suffixes = [
        '儿', '里', 
    ]
    pos = 'r'

# 指南针模型
class compassModel(generalModel):
    roots = [
        ['东'], ['南'], ['西'], ['北'], ['东北'], ['西北'], ['东南'], ['西南'], 
    ]
    pos = 'f'

    # 前缀派生
    def prefixDerivate(self):
        self.roots = [ [ prefix + r for prefix in self.prefixes ] for root in self.roots for r in root]
        return self.roots

    # 后缀派生
    def suffixDerivate(self):
        self.roots = [ [ r + suffix for suffix in self.suffixes ] for root in self.roots for r in root]
        return self.roots

fCompassSuffixDerivations = compassModel('f')
fCompassSuffixDerivations.suffixDerivate()

fCompassPrefixDerivations = compassModel('f')
fCompassPrefixDerivations.prefixes = [
    '正', '以'
]
fCompassPrefixDerivations.prefixDerivate()
    

nzCompassSuffixDerivations = compassModel('nz')
nzCompassSuffixDerivations.suffixes = [
    '麓', '岸', '坡', 
    '山', '海', '湖', 
    '国', '城', '门', '口', '路', '街', '半球'
]
nzCompassSuffixDerivations.suffixDerivate()


# 垂直中线模型
class verticalMidlineModel(generalModel):
    roots = [
        ['中'], ['上'], ['下'], 
    ]
    suffixes = [
        '层', '游'
    ]
    pos = 'f'

    # 前缀派生
    def prefixDerivate(self):
        self.roots = [ [ prefix + r for prefix in self.prefixes ] for root in self.roots for r in root]
        return self.roots

    # 后缀派生
    def suffixDerivate(self):
        self.roots = [ [ r + suffix for suffix in self.suffixes ] for root in self.roots for r in root]
        return self.roots


# 盒子模型、隔断模型
class boxModel(generalModel):
    # 内部关系太复杂，因此没有细分
    ## 例如，roots是可以组合的，而且是按顺序的： 左/右-前/后-上/下-generalSuffixes
    left = [
        ['左'], 
        ['右'], 
    ]
    front = [
        ['前'], 
        ['后'], 
    ]
    top = [
        ['上'], 
        ['下'], 
    ]
    roots = left + front + top + [
        ['里', '内'], 
        ['外'],
        ['底'],
        ['顶'],
        ['侧'],
        # ['进'], ['出'], ['来'], ['去',]
    ]
    compounds = []
    for lr in left:
        for fb in front:
            for tb in top:
                compounds.append([lr[0] + fb[0]])
                compounds.append([lr[0] + tb[0]])
                compounds.append([lr[0] + fb[0] + tb[0]])
    roots += compounds
    prefixes = [
        '之', '以', '侧', 
    ]
    suffixes = [
        '首', '层', 
    ]
    pos = 'f'
    def __init__(self):
        self.framework = {}
        for root in self.roots:
            self.framework[root] = ''

clusterLists = [
    # 指南针模型
    compassModel.roots,
    nzCompassSuffixDerivations.roots,
    fCompassSuffixDerivations.roots,
    fCompassPrefixDerivations.roots,
    # 盒子模型、隔断模型
    boxModel.roots,
    [
        boxModel.general('里') + boxModel.general('内') + ['当中', '之中', '中',],
        boxModel.general('外') + [ '外围', ], 
        boxModel.general('上') + boxModel.general('顶') + [ '底下', ],
        boxModel.general('下') + boxModel.general('底'),
        boxModel.general('左'),
        boxModel.general('右'),
        boxModel.general('前'),
        boxModel.general('后'),
        ['四周', '四面', '四围', '四周围', '周围'],
        ['侧方', '侧面', '侧旁'],
        ['旁', '旁边', '边上', '边沿', '近旁', '近前',],
        ['附近', ], 
    ],
    # 身体模型
    [
        ['身前', '跟前', '面前', ], 
        ['身后', '背后', ], 
        ['身上', ], 
        ['身旁', ], 
        ['眼前'],
        ['胸前', '胸上', ], 
        # ['胸中', '心中', '脑中'], 
        ['头顶', '头上', ], 
        ['手边', ], 
        ['手上', ],
        ['脚上', ], 
        ['脚下', ],
    ],
    # 垂直中线模型
    [
        ['正中', '正当中', '当中', '中部', '中间', '之间', '之中', '中', ],
        ['一旁', ],
        ['两边', '两侧', '两端', '两旁', ],
        ['对面', '斜对面',], 
    ],
    # 水平中线模型
    [
        verticalMidlineModel.general('中') + ['中间', '之间', '之中', '中', ],
        verticalMidlineModel.general('上'),
        verticalMidlineModel.general('下'),
    ],
    # 循环模型
    [
        ['顺时针'], 
        ['逆时针'],
    ],
    # 有限模型
    [
        ['起点'], 
        ['终点', '尽头'],
    ],
    # 沿线模型
    [
        ['沿线', '沿岸', '沿海', ]
    ],
    # 方位指示代词
    indicationWords.generalSuffixDerivate(),
    indicationWords.suffixDerivate(),
    # 趋向介词 
    [
        ['朝', '朝着',], # '冲', '奔', 
        ['从', '自',], # '打', 
        ['到', '至',], # '至于',
        ['经', '经由', ], # '经过', 
        ['距', '离', ], 
        # ['临', ], 
        ['顺', '顺着', '沿', '沿着',], 
        ['往', '向着', '向', ], 
        ['于', '在', ], 
    ],
    
    # 双音节趋向动词（趋向模型）
    [
        ['上来'], ['上去'], ['下来'], ['下去'], ['进来'], ['进去'], ['出来'], ['出去'], ['回来'], ['回去'], ['过来'], ['过去'], ['起来'],
    ],
    # 单音节趋向动词（趋向模型）
    [
        ['上'], ['下'], ['进'], ['出'], ['回'], ['过'], 
    ],
    [
        ['来'], ['去'],
    ],
    # [
    #     ['起'], ['开']
    # ],
    # 联合式方位词
    [
        ['前后'], ['上下'], ['左右'], ['里外'], ['内外'], ['东西'], ['南北'],
    ],
]

entityPos = ['n', 'ns', 'nr', 'nt', 'r', 's']

stopPos = ['t', 'd', 'j']
stopWords = [
    ('过', 'u'),
    ('过', 'v'),
    ('到', 'v'),
    ('离', 'v'),
    ('回', 'q'),
    ('下', 'q'),
    ('出', 'q'),
    ('里', 'q'),
    ('顶', 'q'),
    ('东西', 'n'),
    ('过去', 't'),
    ('在', 'p'),
    ('于', 'p'),
]

scoreMap = {
    'f': 4,
    'v': 3,
    's': 3,
    'p': 2,
}

allPrefixes = set(boxModel.prefixes + generalModel.prefixes + indicationWords.prefixes + compassModel.prefixes + fCompassPrefixDerivations.prefixes)
allSuffixes = set(boxModel.suffixes + generalModel.suffixes + indicationWords.suffixes + compassModel.suffixes + verticalMidlineModel.suffixes + nzCompassSuffixDerivations.suffixes )

