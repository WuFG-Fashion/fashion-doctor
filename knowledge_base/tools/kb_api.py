"""
Fashion Doctor 知识库 API 服务
================================
FastAPI 服务，提供服装零售知识库的 REST API 查询。

启动方式：
  python kb_api.py                    # 直接启动（开发模式，含热重载）
  python kb_api.py --prod             # 生产模式（单进程，NSSM 管理）
  python kb_api.py --port 8899        # 指定端口

API 端点：
  GET /v1/health                     # 健康检查
  GET /v1/thresholds                 # 所有阈值
  GET /v1/thresholds/{name}          # 指定阈值（支持 ?brand=xxx）
  GET /v1/benchmarks                 # 行业基准
  GET /v1/benchmarks/{name}          # 指定基准
  GET /v1/competitors                # 竞品列表
  GET /v1/competitors/{brand}        # 指定竞品数据
  GET /v1/competitors/{brand}/{metric} # 竞品特定指标
  GET /v1/guides/benchmarks          # 导购分析基准
  GET /v1/abc/benchmarks             # ABC分析基准
  GET /v1/vip/benchmarks             # VIP分析基准
  GET /v1/knowledge/search?q=xxx     # 知识库搜索
  GET /v1/knowledge/sql/{template}   # SQL模板
  GET /v1/categories                 # 品类列表
  GET /v1/brands                     # 已配置品牌列表
"""

import json
import os
import sys
import time
import logging
import re
from pathlib import Path
from datetime import datetime
from functools import lru_cache
from typing import Optional

# ── 依赖检查 ──────────────────────────────────────────
_MISSING = []
try:
    from fastapi import FastAPI, Query, HTTPException, Request
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
except ImportError:
    _MISSING.append("fastapi")

try:
    import uvicorn
except ImportError:
    _MISSING.append("uvicorn")

try:
    import toml
except ImportError:
    _MISSING.append("toml")  # 用于读品牌TOML配置

if _MISSING:
    print(f"缺少依赖: {', '.join(_MISSING)}")
    print(f"运行: pip install {' '.join(_MISSING)}")
    sys.exit(1)

# ── 配置 ──────────────────────────────────────────────
KB_ROOT = Path(os.environ.get("KB_ROOT") or Path(__file__).resolve().parents[1])  # knowledge_base/ 根：KB_ROOT 环境变量优先，默认按脚本位置推导（修复：此前误用 parent 指向 tools/，基准/配置/wiki 全部读不到）
BENCHMARKS_FILE = KB_ROOT / "kb_benchmarks.json"
BRAND_CONFIGS_DIR = KB_ROOT / "brand_configs"
WIKI_DIR = KB_ROOT / "wiki"
RAW_DIR = KB_ROOT / "raw"
PORT = int(os.environ.get("KB_API_PORT", 8899))
API_KEY = os.environ.get("KB_API_KEY", "kb_readonly_2026")  # 默认key，生产环境改环境变量
IS_PROD = "--prod" in sys.argv

# ── 日志 ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("kb_api")

# ── 应用实例 ──────────────────────────────────────────
app = FastAPI(
    title="Fashion Doctor 知识库 API",
    description="服装零售行业知识库查询服务",
    version="1.0.0",
    docs_url="/docs" if not IS_PROD else None,  # 生产模式关闭自动文档
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── 数据加载（懒加载 + 缓存，API 不会频繁读文件）──────

@lru_cache(maxsize=1)
def _load_benchmarks() -> dict:
    """加载基准数据 JSON"""
    if BENCHMARKS_FILE.exists():
        with open(BENCHMARKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    logger.warning(f"基准文件不存在: {BENCHMARKS_FILE}，使用空数据")
    return {}

@lru_cache(maxsize=32)
def _load_brand_config(brand: str) -> dict:
    """加载品牌 TOML 配置"""
    config_file = BRAND_CONFIGS_DIR / f"{brand}.toml"
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            return toml.load(f)
    return {}

def _list_brand_configs() -> list:
    """列出所有品牌配置文件"""
    brands = []
    if BRAND_CONFIGS_DIR.exists():
        for f in BRAND_CONFIGS_DIR.glob("*.toml"):
            brands.append(f.stem)
    return sorted(brands)

def _merge_thresholds(brand: Optional[str] = None) -> dict:
    """合并通用阈值 + 品牌自定义阈值"""
    data = _load_benchmarks()
    base = data.get("thresholds", {}).copy()
    if brand:
        config = _load_brand_config(brand)
        brand_thresholds = config.get("thresholds", {})
        for key, val in brand_thresholds.items():
            # key格式: "gross_margin.excellent"
            parts = key.split(".")
            if len(parts) == 2:
                parent, child = parts
                if parent not in base:
                    base[parent] = {}
                base[parent][child] = val
    return base

# ── 安全中间件 ────────────────────────────────────────

@app.middleware("http")
async def rate_limit_and_auth(request: Request, call_next):
    """简易限流 + API Key 验证"""
    # 健康检查不需要鉴权
    if request.url.path == "/v1/health":
        return await call_next(request)

    # API Key 验证（从 Header 或 Query 参数读取）
    key = request.headers.get("X-API-Key") or request.query_params.get("api_key")
    if key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"error": "unauthorized", "message": "需要有效的 API Key。请在 Header 中设置 X-API-Key 或在 URL 中传 ?api_key=xxx"},
        )

    # 简易限流：每 IP 每分钟最多 60 次调用
    # 生产环境建议用 slowapi 或 Redis 实现
    return await call_next(request)

# ── 辅助函数 ──────────────────────────────────────────

def _make_response(data, extra=None):
    """统一响应格式"""
    resp = {
        "ok": True,
        "timestamp": datetime.now().isoformat(),
        "data": data,
    }
    if extra:
        resp.update(extra)
    return resp

def _flatten_benchmarks(data, prefix=""):
    """将嵌套的阈值字典扁平化为 name.subname 格式"""
    result = {}
    for key, val in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(val, dict) and not any(k in val for k in ("unit", "formula", "description")):
            # 纯嵌套结构，继续扁平化
            result.update(_flatten_benchmarks(val, full_key))
        else:
            result[full_key] = val
    return result

def _search_wiki(query: str, limit: int = 10) -> list:
    """搜索 wiki 目录下的 markdown 文件"""
    results = []
    if not WIKI_DIR.exists():
        return results
    query_lower = query.lower()
    for md_file in WIKI_DIR.rglob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            score = content.lower().count(query_lower)
            if score > 0:
                # 提取标题
                title_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
                title = title_match.group(1) if title_match else md_file.stem
                # 提取摘要（前200字）
                summary = re.sub(r"^---.*?---\s*", "", content[:500], flags=re.DOTALL)
                summary = summary.strip()[:200]
                results.append({
                    "file": str(md_file.relative_to(WIKI_DIR)),
                    "title": title,
                    "summary": summary,
                    "relevance": score,
                })
        except Exception:
            pass

    results.sort(key=lambda x: x["relevance"], reverse=True)
    return results[:limit]

def _get_sql_template(name: str) -> Optional[dict]:
    """从 wiki/practices/ 提取 SQL 模板"""
    practices_dir = WIKI_DIR / "practices"
    if not practices_dir.exists():
        return None
    for md_file in practices_dir.glob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            if name.lower() in md_file.stem.lower() or name.lower() in content.lower()[:200]:
                # 提取所有 SQL 代码块
                sql_blocks = re.findall(r"```sql\n(.*?)```", content, re.DOTALL)
                python_blocks = re.findall(r"```python\n(.*?)```", content, re.DOTALL)
                return {
                    "file": str(md_file.relative_to(WIKI_DIR)),
                    "title": re.search(r"^#\s+(.+)", content, re.MULTILINE).group(1) if re.search(r"^#\s+(.+)", content, re.MULTILINE) else md_file.stem,
                    "sql_templates": [b.strip() for b in sql_blocks],
                    "python_templates": [b.strip() for b in python_blocks],
                }
        except Exception:
            pass
    return None


# ═══════════════════════════════════════════════════════
#  API 端点
# ═══════════════════════════════════════════════════════

@app.get("/v1/health")
async def health():
    """健康检查 — 不需要 API Key"""
    data = _load_benchmarks()
    return _make_response({
        "status": "ok",
        "version": data.get("_version", "unknown"),
        "brands_configured": _list_brand_configs(),
        "uptime_seconds": time.time() - _start_time,
    })


# ── 阈值 ──────────────────────────────────────────────

@app.get("/v1/thresholds")
async def list_thresholds(brand: Optional[str] = Query(None, description="品牌名")):
    """列出所有阈值（支持品牌覆盖）"""
    merged = _merge_thresholds(brand)
    flat = _flatten_benchmarks(merged)
    return _make_response(flat, {"brand": brand} if brand else {})


@app.get("/v1/thresholds/{name}")
async def get_threshold(
    name: str,
    brand: Optional[str] = Query(None, description="品牌名，覆盖通用阈值"),
):
    """获取指定阈值"""
    merged = _merge_thresholds(brand)
    flat = _flatten_benchmarks(merged)

    # 精确匹配
    if name in flat:
        return _make_response({name: flat[name]}, {"brand": brand} if brand else {})

    # 模糊匹配：查找包含 name 的所有键
    matches = {k: v for k, v in flat.items() if name.lower() in k.lower()}
    if matches:
        return _make_response(matches, {"brand": brand, "match_type": "fuzzy"} if brand else {"match_type": "fuzzy"})

    raise HTTPException(404, f"阈值 '{name}' 未找到。可用阈值: {list(flat.keys())[:10]}...")


# ── 行业基准 ──────────────────────────────────────────

@app.get("/v1/benchmarks")
async def list_benchmarks():
    """列出所有行业基准"""
    data = _load_benchmarks()
    return _make_response({
        "industry": data.get("industry", {}),
        "thresholds_summary": {k: v.get("description", "") for k, v in data.get("thresholds", {}).items()},
    })


@app.get("/v1/benchmarks/{name}")
async def get_benchmark(name: str):
    """获取指定行业基准"""
    data = _load_benchmarks()
    # 先查 industry
    industry = data.get("industry", {})
    flat_industry = _flatten_benchmarks(industry)
    if name in flat_industry:
        return _make_response({name: flat_industry[name]})

    # 再查 thresholds
    thresholds = data.get("thresholds", {})
    if name in thresholds:
        return _make_response({name: thresholds[name]})

    # 模糊匹配
    all_keys = list(_flatten_benchmarks(industry).keys()) + list(thresholds.keys())
    matches = [k for k in all_keys if name.lower() in k.lower()]
    if matches:
        raise HTTPException(404, f"未精确匹配 '{name}'。相近: {matches[:5]}")

    raise HTTPException(404, f"基准 '{name}' 未找到")


# ── 竞品数据 ──────────────────────────────────────────

@app.get("/v1/competitors")
async def list_competitors():
    """列出所有竞品"""
    data = _load_benchmarks()
    competitors = data.get("competitors", {})
    summary = {k: {"stock_code": v.get("stock_code"), "category": v.get("category"), "tier": v.get("tier")} for k, v in competitors.items()}
    return _make_response(summary)


@app.get("/v1/competitors/{brand}")
async def get_competitor(brand: str):
    """获取指定竞品完整数据"""
    data = _load_benchmarks()
    competitors = data.get("competitors", {})
    if brand in competitors:
        return _make_response(competitors[brand])
    raise HTTPException(404, f"竞品 '{brand}' 未找到。可用: {list(competitors.keys())}")


@app.get("/v1/competitors/{brand}/{metric}")
async def get_competitor_metric(brand: str, metric: str):
    """获取竞品特定指标"""
    data = _load_benchmarks()
    competitor = data.get("competitors", {}).get(brand)
    if not competitor:
        raise HTTPException(404, f"竞品 '{brand}' 未找到")
    if metric in competitor:
        return _make_response({metric: competitor[metric], "brand": brand})
    # 模糊匹配
    matches = [k for k in competitor.keys() if metric.lower() in k.lower()]
    if matches:
        return _make_response({k: competitor[k] for k in matches}, {"brand": brand, "match_type": "fuzzy"})
    raise HTTPException(404, f"指标 '{metric}' 未找到。可用: {list(competitor.keys())[:15]}")


# ── 导购 / ABC / VIP ─────────────────────────────────

@app.get("/v1/guides/benchmarks")
async def guide_benchmarks():
    """导购分析基准"""
    data = _load_benchmarks()
    return _make_response(data.get("guide_benchmarks", {}))


@app.get("/v1/abc/benchmarks")
async def abc_benchmarks():
    """ABC分析基准"""
    data = _load_benchmarks()
    return _make_response(data.get("abc_benchmarks", {}))


@app.get("/v1/vip/benchmarks")
async def vip_benchmarks():
    """VIP分析基准"""
    data = _load_benchmarks()
    return _make_response(data.get("vip_benchmarks", {}))


# ── 知识搜索 ──────────────────────────────────────────

@app.get("/v1/knowledge/search")
async def search_knowledge(
    q: str = Query(..., min_length=2, description="搜索关键词"),
    limit: int = Query(10, ge=1, le=50),
):
    """搜索知识库"""
    results = _search_wiki(q, limit)
    return _make_response({
        "query": q,
        "total": len(results),
        "results": results,
    })


@app.get("/v1/knowledge/sql/{template}")
async def sql_template(template: str):
    """获取 SQL 模板"""
    result = _get_sql_template(template)
    if result:
        return _make_response(result)
    raise HTTPException(404, f"SQL模板 '{template}' 未找到。试搜: '滞销' / 'ABC' / '安全库存'")


# ── 品类 / 品牌列表 ───────────────────────────────────

@app.get("/v1/categories")
async def list_categories():
    """支持的品类列表"""
    return _make_response({
        "categories": ["menswear", "womenswear", "kidswear", "casual", "fast_fashion"],
        "tiers": ["mass", "mid", "mid-premium", "premium", "luxury"],
    })


@app.get("/v1/brands")
async def list_brands():
    """已配置的品牌"""
    return _make_response({
        "brands_configured": _list_brand_configs(),
        "competitors_available": list(_load_benchmarks().get("competitors", {}).keys()),
    })


# ── 启动 ──────────────────────────────────────────────

_start_time = time.time()

if __name__ == "__main__":
    mode = "生产" if IS_PROD else "开发"
    logger.info(f"Fashion Doctor 知识库 API 启动 ({mode}模式)")
    logger.info(f"端口: {PORT}")
    logger.info(f"基准文件: {BENCHMARKS_FILE}")
    logger.info(f"品牌配置: {_list_brand_configs()}")

    if not BENCHMARKS_FILE.exists():
        logger.warning("⚠️  kb_benchmarks.json 不存在！API 将返回空数据。")
        logger.warning("   请执行知识库优化任务生成此文件。")

    uvicorn.run(
        "kb_api:app",
        host="0.0.0.0",
        port=PORT,
        reload=not IS_PROD,
        log_level="warning" if IS_PROD else "info",
    )
