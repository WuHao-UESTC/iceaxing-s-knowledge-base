# CLAUDE.md — 知识库根目录配置

## 项目概述

本仓库是一个 **Obsidian 知识库（vault）**，按门类（知识领域）组织为多个子知识体系。每个门类下有自己的 `CLAUDE.md` 框架级配置，以及（教材类门类）`知识导图.md` 概念索引中枢。

主要知识门类（含 `CLAUDE.md`）：

| 门类 | 领域 |
|------|------|
| `Communication/` | 通信系统 |
| `Digital Design/` | 数字设计 |
| `IC/` | 集成电路（模拟 IC、数字 IC、RF IC、工艺与封装） |
| `Magneticelectro Theory/` | 电磁理论 |
| `IELTS/口语语料库/` | 雅思口语语料库 |

其余目录（`Datasheet/`、`Reading Note/`、`Diary/`、`Tasks/`、`System/`、竞赛与规划类目录等）为非教材类资料，不属于本约定的教材插槽范围。

---

## 教材位置约定（重要）

所有门类的**教材 markdown 源文件**统一存放在一个独立的 `_textbook-md` 目录中。该目录**不在本知识库内**，而是位于各主机的用户目录下，例如：

| 主机 | `_textbook-md` 绝对路径 |
|------|------------------------|
| Windows | `E:\_textbook-md\` |
| Linux | `/home/iceaxing/MyDoc/_textbook-md/` |

**核心规则**：

1. 教材相对于 `_textbook-md` 的**相对路径在两台主机上完全相同**——即 `_textbook-md/` 之下的子目录结构、文件名都是一致的。
2. 只有 `_textbook-md` 这个**文件夹的绝对路径**在两台主机上不同。
3. 因此，任意一本教材，只要知道它在 `_textbook-md` 下的相对路径，即可由上述两个前缀拼出对应主机上的完整路径。

> 例：教材相对路径为 `Signal and System/textbook/`，则
> - Windows：`E:\_textbook-md\Signal and System\textbook\`
> - Linux：`/home/iceaxing/MyDoc/_textbook-md/Signal and System/textbook/`
>
> 相对路径不变，仅前缀不同。

---

## 新教材接入要求

每次在**任意门类的 `CLAUDE.md` 教材插槽（或课本插槽）中新增一本教材**时，必须**同时给出 Windows 与 Linux 两台主机上的教材位置**，并保持两行中的相对路径一致。统一格式如下：

```markdown
**教材位置**：
- **Windows**：`E:\_textbook-md\<相对路径>`
- **Linux**：`/home/iceaxing/MyDoc/_textbook-md/<相对路径>`
```

其中 `<相对路径>` 在 Windows 与 Linux 两行中保持一致（Windows 用反斜杠 `\`，Linux 用正斜杠 `/`）。
