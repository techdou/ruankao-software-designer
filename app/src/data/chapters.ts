// 章节体系：按官方考纲知识域组织（对应第5版教材章节，重新按备考效率分章）
import type { ChapterMeta } from '../core/types'

export const CHAPTERS: ChapterMeta[] = [
  {
    id: 'ch01',
    title: '计算机系统基础',
    subtitle: 'CPU 组成 · 存储系统 · 校验码 · 可靠性',
    weight: 6,
    keyPoints: ['原码/反码/补码/移码', '浮点数表示与规格化', 'Cache 命中率与平均访存时间', '海明码与 CRC 校验', '系统可靠性串联并联'],
  },
  {
    id: 'ch02',
    title: '计算机体系结构',
    subtitle: '指令系统 · 流水线 · 多处理机 · 嵌入式',
    weight: 5,
    keyPoints: ['CISC 与 RISC 对比', '流水线执行时间/吞吐率/加速比', '总线与中断（中断向量、中断响应）', 'RAID 级别', '嵌入式系统与实时操作系统'],
  },
  {
    id: 'ch03',
    title: '程序设计语言基础',
    subtitle: '编译原理 · 文法 · 参数传递 · 语言特性',
    weight: 5,
    keyPoints: ['编译与解释', '正则式与有限自动机', '文法推导与语法树', '传值调用 vs 引用调用', '静态/动态作用域与闭包'],
  },
  {
    id: 'ch04',
    title: '数据结构',
    subtitle: '线性表 · 栈队列 · 树 · 图 · 查找 · 排序',
    weight: 8,
    keyPoints: ['循环队列判满判空', '二叉树性质与遍历还原', 'Huffman 树与编码', '图的存储/遍历/最小生成树/最短路', '各排序算法对比与稳定性', '二分查找与散列表冲突处理'],
  },
  {
    id: 'ch05',
    title: '操作系统',
    subtitle: '进程管理 · 存储管理 · 文件与设备',
    weight: 6,
    keyPoints: ['进程三态/五态转换', 'PV 操作与信号量', '死锁四条件与银行家算法', '页式/段式/段页式地址变换', '页面置换算法（LRU/FIFO）', '磁盘调度与位示图'],
  },
  {
    id: 'ch06',
    title: '软件工程基础',
    subtitle: '过程模型 · 需求 · 设计原则 · 测试 · 项目管理',
    weight: 10,
    keyPoints: ['瀑布/原型/敏捷/螺旋模型选型', '需求分析与软件质量特性（McCall/ISO）', '内聚耦合七级', 'McCabe 环形复杂度', '黑盒/白盒测试', '关键路径与甘特图', 'CMM/CMMI 成熟度'],
  },
  {
    id: 'ch07',
    title: '结构化开发方法',
    subtitle: 'DFD 数据流图 · 结构图 · 模块设计',
    weight: 4,
    keyPoints: ['DFD 元素与分层细化', '数据字典条目', '变换型/事务型分析', '模块作用域与控制域'],
  },
  {
    id: 'ch08',
    title: '面向对象技术',
    subtitle: 'OOA/OOD · UML 十三图 · 23 种设计模式',
    weight: 10,
    keyPoints: ['面向对象七大原则', 'UML 用例/类/顺序/状态/活动图', '类间关系（泛化/实现/关联/聚合/组合/依赖）', '创建型/结构型/行为型模式识别', '重载/重写与多态绑定'],
  },
  {
    id: 'ch09',
    title: '算法设计与分析',
    subtitle: '渐进分析 · 五大策略 · 经典算法',
    weight: 5,
    keyPoints: ['大 O 时间复杂度比较', '分治（归并/二分）', '贪心 vs 动态规划识别', '回溯与分支限界（解空间搜索方式）', '背包/LCS/矩阵连乘'],
  },
  {
    id: 'ch10',
    title: '数据库技术',
    subtitle: '三级模式 · ER 模型 · 关系代数 · SQL · 规范化 · 事务',
    weight: 6,
    keyPoints: ['三级模式两级映像', 'ER 图转关系模式', '自然连接等关系代数', 'SQL DDL/DQL（分组聚合嵌套）', '函数依赖与范式判定', 'ACID 与并发控制（锁协议）', '转储与日志恢复'],
  },
  {
    id: 'ch11',
    title: '计算机网络',
    subtitle: 'OSI/TCP-IP · IP 地址与子网 · 常用协议',
    weight: 5,
    keyPoints: ['七层模型设备归属', '子网划分与聚合（掩码计算）', 'TCP/UDP 与三次握手', 'DHCP/DNS/HTTP/FTP 端口', '路由器 vs 交换机', 'IPv6 基础'],
  },
  {
    id: 'ch12',
    title: '信息安全',
    subtitle: '密码学 · 数字签名 · 攻击防御 · 恶意代码',
    weight: 4,
    keyPoints: ['对称 vs 非对称加密算法', '报文摘要与数字签名流程', '数字证书与 CA', 'DoS/DDoS/SQL注入/XSS', '防火墙与入侵检测', '计算机病毒与木马'],
  },
  {
    id: 'ch13',
    title: '知识产权与标准化',
    subtitle: '著作权 · 专利 · 商标 · 标准分级',
    weight: 3,
    keyPoints: ['软件著作权归属（职务作品/委托开发/合作开发）', '保护期限速记表', '专利先申请原则', '商标注册在先与续展', '国际/国家/行业/地方标准代号'],
  },
  {
    id: 'ch14',
    title: '数学与专业英语',
    subtitle: '离散逻辑 · 排列组合 · 图论 · 英语题技巧',
    weight: 4,
    keyPoints: ['命题逻辑等价与推理', '排列组合与鸽巢', '线性规划图解', '专业英语 5 题定位词法', '高频英语术语表'],
  },
]

export const chapterMap = new Map(CHAPTERS.map((c) => [c.id, c]))
