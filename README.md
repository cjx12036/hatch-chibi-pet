# Hatch Chibi Pet 🐣

把任意单人照片变成可安装的 **Q 版 Codex 动态桌宠**。

Turn any portrait into an installable **animated chibi pet for Codex**.

[![Release](https://img.shields.io/github/v/release/cjx12036/hatch-chibi-pet?include_prereleases)](https://github.com/cjx12036/hatch-chibi-pet/releases)
[![License](https://img.shields.io/github/license/cjx12036/hatch-chibi-pet)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827)](skill/hatch-chibi-pet/SKILL.md)

<p align="center">
  <img src="assets/demo/idle.gif" width="180" alt="YJY chibi pet idle animation">
</p>

## 它能做什么

- 默认生成约 **2.5 头身**的大头 Q 版人物，而不是缩小的写实成年人。
- 保留眼镜、发型、辫子、服装配色等人物识别特征。
- 自动生成 Codex 所需的 9 种状态：待机、左右跑动、挥手、跳跃、失败、等待、工作中和审阅。
- 输出标准 `1536×1872` 透明 WebP 精灵图，固定为 `8×9` 网格、每格 `192×208`。
- 使用稳定槽位、双重绿幕清理、逐帧 QA 和动作比例归一化，减少绿边、碎片、跳帧与人物忽大忽小。
- 自动打包并安装到 `~/.codex/pets/<pet-id>/`。

## 动画示例

| 待机 Idle | 挥手 Waving | 跳跃 Jumping | 跑动 Running |
| --- | --- | --- | --- |
| ![Idle](assets/demo/idle.gif) | ![Waving](assets/demo/waving.gif) | ![Jumping](assets/demo/jumping.gif) | ![Running](assets/demo/running-right.gif) |

完整 9 行动作表：

![YJY contact sheet](assets/demo/contact-sheet.png)

> 示例仓库只包含生成结果，不包含人物原始照片。

## 安装

### 方式一：下载 Release

从 [Releases](https://github.com/cjx12036/hatch-chibi-pet/releases/latest) 下载 `hatch-chibi-pet.zip`，解压到：

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
4. 两次清除绿幕与低透明色点，稳定槽位切帧。
5. 生成动作表和 GIF，进行结构与独立视觉验收。
6. 输出 `pet.json` 与 `spritesheet.webp` 并安装。

## 仓库结构

```text
skill/hatch-chibi-pet/   可直接安装的 Codex Skill
assets/demo/             README 动画与动作表
```

## English

Hatch Chibi Pet is a reusable Codex Skill that turns a single-person reference photo into a consistent, animated chibi desktop pet. It generates the complete nine-state Codex atlas, performs deterministic frame assembly and two-pass chroma cleanup, validates transparency and geometry, visually checks motion, and installs the result locally.

Upload a portrait and ask:

```text
Use $hatch-chibi-pet to turn this person into an animated chibi Codex pet and install it.
```

## Requirements

- Codex with the built-in `$imagegen` skill
- Python 3 with Pillow
- `jq`

Only use photos you have permission to process. Avoid publishing source portraits or generated likenesses without the person's consent.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). When reporting visual bugs, share the generated contact sheet and validation JSON when possible; do not attach private source portraits.

If this project is useful, consider starring the repository and sharing a generated pet demo. ⭐

## License

Apache License 2.0. See [LICENSE](LICENSE) and the bundled skill [NOTICE](skill/hatch-chibi-pet/NOTICE).
