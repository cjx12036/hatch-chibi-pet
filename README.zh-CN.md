# Hatch Chibi Pet 🐣

[English](README.md) | **简体中文**

把任意单人照片变成可安装的 **Q 版 Codex 动态桌宠**。

[![Release](https://img.shields.io/github/v/release/cjx12036/hatch-chibi-pet?include_prereleases)](https://github.com/cjx12036/hatch-chibi-pet/releases)
[![License](https://img.shields.io/github/license/cjx12036/hatch-chibi-pet)](LICENSE)
[![Validate Skill](https://github.com/cjx12036/hatch-chibi-pet/actions/workflows/validate.yml/badge.svg)](https://github.com/cjx12036/hatch-chibi-pet/actions/workflows/validate.yml)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827)](skill/hatch-chibi-pet/SKILL.md)

<p align="center">
  <img src="assets/demo/idle.gif" width="180" alt="YJY Q 版桌宠待机动画">
</p>

## 它能做什么

- 默认生成约 **2.5 头身**的大头 Q 版人物，而不是缩小的写实成年人。
- 保留眼镜、发型、辫子、服装配色等人物识别特征。
- 自动生成 Codex 所需的 9 种状态：待机、向左跑、向右跑、挥手、跳跃、失败、等待、工作中和审阅。
- 输出标准 `1536×1872` 透明 WebP 精灵图，固定为 `8×9` 网格、每格 `192×208`。
- 使用稳定槽位、双重绿幕清理、逐帧 QA 和动作比例归一化，减少绿边、碎片、跳帧与人物忽大忽小。
- 自动打包并安装到 `~/.codex/pets/<pet-id>/`。

## 动画示例

| 待机 | 挥手 | 跳跃 | 跑动 |
| --- | --- | --- | --- |
| ![待机](assets/demo/idle.gif) | ![挥手](assets/demo/waving.gif) | ![跳跃](assets/demo/jumping.gif) | ![跑动](assets/demo/running-right.gif) |

完整 9 行动作表：

![YJY 完整动作表](assets/demo/contact-sheet.png)

> 示例仓库只包含生成结果，不包含人物原始照片。

## 安装

### 方式一：下载 Release

从[最新版本](https://github.com/cjx12036/hatch-chibi-pet/releases/latest)下载 `hatch-chibi-pet.zip`，然后解压到：

```text
~/.codex/skills/hatch-chibi-pet/
```

### 方式二：Git Clone

```bash
git clone https://github.com/cjx12036/hatch-chibi-pet.git
mkdir -p ~/.codex/skills
cp -R hatch-chibi-pet/skill/hatch-chibi-pet ~/.codex/skills/
```

建议安装后新建一个 Codex 任务，让 Skill 被重新发现。

## 使用

上传一张清晰的单人照片，然后输入：

```text
使用 $hatch-chibi-pet 把这个人物制作成 Q 版 Codex 动态桌宠并安装。
```

也可以直接指定名字：

```text
使用 $hatch-chibi-pet 把这个人物制作成 Q 版桌宠，新人物叫 YJY。
```

完成后进入 Codex：

```text
Settings → Pets → Refresh → 选择新桌宠 → Show pet
```

## 工作流程

1. 分析照片，提取 3–6 个人物识别锚点。
2. 生成固定 Q 版比例的主视觉。
3. 分别生成 9 行动画，左右跑动默认独立生成。
4. 两次清除绿幕溢色与低透明色点，再使用稳定槽位切帧。
5. 生成动作表和 GIF，进行结构与独立视觉验收。
6. 输出 `pet.json` 与 `spritesheet.webp` 并安装。

## 仓库结构

```text
skill/hatch-chibi-pet/   可直接安装的 Codex Skill
assets/demo/             README 动画与动作表
```

## 环境要求

- 带有内置 `$imagegen` Skill 的 Codex
- 安装了 Pillow 的 Python 3
- `jq`

请只处理你有权使用的照片。未经本人同意，请勿公开原始照片或生成的人物形象。

## 参与贡献

欢迎提交 Issue 和 Pull Request，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。报告视觉问题时，请尽可能附上生成的动作表和验证 JSON，不要上传私人原始照片。

如果这个项目对你有帮助，欢迎点亮 Star，并分享你生成的桌宠演示。⭐

## 许可证

本项目使用 Apache License 2.0，详见 [LICENSE](LICENSE) 和 Skill 内附的 [NOTICE](skill/hatch-chibi-pet/NOTICE)。
