---
title: brand_wall 品牌墙说明
layer: T0
scope: public
status: active
---

# brand_wall — 品牌墙（跨公司共享品牌参考层）

原 MODING 运营代理操盘的品牌集合 + 双核（卡宾/太平鸟）+ 重点补充女装（艾诺丝/迪卡轩），共 35 个 focus_brands（机器可读清单见根目录 `kb_benchmarks.json` 的 `focus_brands`）。

- **只增不减**：品牌墙是跨公司公共可读层；公司域（如 `40_companies/dongshang/`）按各自 `company.yaml` 的 `read_brands` 从此读取所需品牌
- **内容在哪**：品牌的实体页/情报页目前编译在 `30_wiki/entities/` 与 `30_wiki/sources/`（`scope: brand` 字段标识）；本目录 `_configs/` 存品牌级配置（如 peacebird.toml）
- **卡宾/太平鸟是独立上市公司/品牌，不挂任何"集团旗下"**；东尚只是「重点读取」这两个品牌
- 后续若品牌级资料增厚到需要独立子目录（如 `brand_wall/cabbeen/`），按 specs §2 树逐个品牌迁建，人批后执行
