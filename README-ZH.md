# byBias-Icons-Packet 📦

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Author](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F%20by%20Francesco-blueviolet) [![GitLab mirror](https://img.shields.io/badge/mirror-GitLab-FC6D26?logo=gitlab&logoColor=white)](https://gitlab.com/FranzBias/byBias-Icons-Paket)
![GitHub stars](https://img.shields.io/github/stars/FranzBias/byBias-Icons-Paket?style=flat) ![GitHub issues](https://img.shields.io/github/issues/FranzBias/byBias-Icons-Paket) [![Donate](https://img.shields.io/badge/Donate-PayPal-00457C?logo=paypal)](https://www.paypal.com/donate/?hosted_button_id=HUF5MYDG465RY)

![byBias-Icons-Packet 图标](icons-packet.svg)

<p align="center">
  <img src="screenshots/01-dashboard.png" width="45%" alt="byBias-Icons-Packet: dashboard">
  <img src="screenshots/02-main-flow.png" width="45%" alt="byBias-Icons-Packet: main flow actions">
</p>

**一款统一的 GTK 应用，用于在 Linux Mint / Cinnamon 上管理个人图标收藏。**

🇬🇧 [README-EN.md](README-EN.md) · 🇮🇹 [README-IT.md](README-IT.md) · 🇩🇪 [README-DE.md](README-DE.md) · 🇪🇸 [README-ES.md](README-ES.md) · 🇫🇷 [README-FR.md](README-FR.md) · 🇳🇱 [README-NL.md](README-NL.md) · 🇷🇺 [README-RU.md](README-RU.md) · 🇸🇦 [README-AR.md](README-AR.md) · 🇨🇳 [README-ZH.md](README-ZH.md) · 🇯🇵 [README-JA.md](README-JA.md)

---

## 💛 一段坦诚的话

> 过去几个月，我一直处于困境：接的活太少，而仅有的那些报酬也太低。如果情
> 况近期没有好转，我将不得不另谋出路——这没什么不好，但我更希望能继续开
> 发像这样的项目。
>
> 如果 **byBias-Icons-Packet** 对你有用，并且你愿意支持它：哪怕只是一欧
> 元的捐赠，只要参与的人足够多，也能带来真正的改变。如果你无法捐赠，**
> 帮忙宣传**同样非常有帮助。无论如何，衷心感谢你读到这里。🙏

---

**byBias-Icons-Packet** 将整套 byBias 图标工具集整合到一个 GTK3 应用
中，专为管理*你自己的*图标收藏而生：提取、清理、统一命名，并制作成主题。
一套用本应用制作的自由图标主题（GPL-3）即将推出。主窗口是一个仪表
盘：每个操作都是一张可见的卡片，点击后会在同一窗口中打开其面板——无需在
菜单中翻找，也无需记忆命令。

## 功能

**主要流程**涵盖了从头到尾创建和维护图标主题的日常工作：

- **提取图标** — 从 `.ico`、`.exe`、`.dll`、`.icl` 文件（即使已重命名以
  伪装成其他类型）中提取图标，重建带透明度的干净 PNG。当下载的图标包实
  际上是伪装过的 Windows 可执行文件时特别有用。
- **创建 / 更新主题** — 将源文件夹复制为一个真正的图标主题：清理文件和
  文件夹名称（空格/下划线 → 连字符，去除重音符号），生成正确的
  `index.theme` 并重建缓存，还可以一键在全系统范围内激活该主题。
- **应用图标** — 一个按*你自己的*分类（而非系统通用分类）组织的选择器，
  让你以可视化方式浏览收藏，并将任意图标应用到文件夹。
- **符号图标** — 将彩色 PNG 转换为单色 16×16 的"符号"SVG 图标，即面板
  和菜单中使用的那种，能根据浅色或深色主题自动变色。
- **猎巨人** — 扫描你的图标与系统图标之间的命名冲突；命名冲突正是图标突
  然显示为巨大尺寸，或显示为图片损坏三角形的经典原因。
- **全部加前缀** — 安全、免维护的选项：为主题中的每个图标添加
  `bybias-` 前缀，使其永远不会意外替换系统图标。
- **替换系统图标** — 选择一个系统槽位（回收站已满/已空、通用文件夹、主
  目录文件夹等）和你自己的一张图片：它将以精确的标准名称安装，从而在桌
  面上该图标出现的所有位置取而代之。
- **在 Nemo 中右键** — *更改图标…* 打开你的收藏并将图标应用到所选文件夹或文件；*粘贴图标* 使用剪贴板中的图像。由 `install.sh` 安装（在 Nemo 中按 F5 即可看到新图标）。

除了主要流程外，仪表盘还将更专业的工具归入四个板块，每个板块都针对一种
特定的困扰：

**维护** — 长期保持庞大收藏的整洁。
- *查找重复项* 按图像的实际内容（像素的哈希值）而非文件名比较图标，从而
  找出以不同名称保存了两次的同一图标。
- *样张总览* 将整个收藏渲染成一张带标注的 PNG 拼贴图——这是真正有用的方
  式，能让你一眼*看到*自己拥有什么，而不必逐个文件夹点击查看。
- *查找相似项* 以一个参考图标为基准，按主色调的接近程度为收藏中的其余图
  标排序，有助于构建视觉上协调一致的子集。

**制作** — 为实际使用打磨图标。
- *标准化尺寸* 以一张尺寸过大的源 PNG 为基础，生成完整的标准尺寸集
  （16 到 256 px），经过恰当缩放，而不是任由系统在运行时粗糙地缩放。
- *重新着色 / 反转* 为单色图标应用所选色调，或反转明暗，从而使符号图标
  集能够适配相反的主题。
- *裁剪并居中* 去除不均匀的透明边距并重新居中图标，应用统一的内边距——
  这正是解决一套混合图标看起来莫名"有点歪"的方法。

**分发** — 分享你构建的成果。
- *导出软件包* 将主题连同自动生成的 `LICENSE` 和 `README` 一起打包为压
  缩包，随时可供发布。
- *生成展示图* 从一组精选图标中构建宣传图片，正是你会想放在下载页面上
  的那种。

**安全与便捷** — 安全网。
- *备份 / 恢复* 在进行有风险的更改前，为主题创建一个带时间戳的快照，一
  旦出现问题，可一键恢复。
- *健康检查* 让整个主题经过一份诊断检查清单（继承关系、带重音符号的名
  称、命名冲突、缓存有效性），在问题演变成巨型图标或图片损坏三角形*之
  前*就将其标记出来。

窗口左上角的菜单（☰）可快速访问**关于**（包含 GitHub 链接）、覆盖此
README 全部 10 种语言的**语言切换器**，以及应用自身的**浅色/深色主
题**开关。

## 依赖

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-xapp-1.0 python3-pil icoutils python3-icoextract
```

首次运行时，如果缺少任何依赖，byBias-Icons-Packet 会检测到，准确列出所
需内容，征求你的明确同意，然后通过系统自身的图形化身份验证（pkexec）或
sudo 进行安装——因此你也可以直接启动它，让它自行完成配置。你的密码始终
由系统处理，绝不会经过该应用。

## 运行

```bash
python3 icons-packet
```

**结构** — `icons_packet_core.py` 包含全部逻辑（不依赖 GTK，可独立测
试）；`icons_packet_gui.py` 是 GTK3 仪表盘；`icons-packet` 是启
动器，也负责上述依赖检查。

**命名规范** — 文件和文件夹名称仅使用连字符（`-`），绝不使用空格或下划
线；应用每次处理主题时都会自动转换这两者。

## 🌱 犯错乃人之常情

这个项目是由一个人在业余时间快速搭建的——因此完全有可能仍存在一些不完
善之处：一个 bug、某个奇怪的行为、一处翻译错误的字符串，甚至是这份
README 本身的某句不够准确的话。如果你发现任何问题，请
提交一个 issue——无论是错误报告、语言更正，还是一般性
的不准确之处，都真诚欢迎。**功能请求**同样如此：如果你希望这个应用做些
什么，或以不同的方式去做，尽管说出来。你的建议将决定这个项目接下来的方
向。

---

*由 FranzBias 用 ❤️ 制作 — [github.com/FranzBias/byBias-Icons-Paket](https://github.com/FranzBias/byBias-Icons-Paket)*
