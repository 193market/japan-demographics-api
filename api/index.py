from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime

app = FastAPI(
    title="Japan Demographics API",
    description="Real-time Japan demographic data powered by World Bank Open Data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WB_BASE_URL = "https://api.worldbank.org/v2/country/JP/indicator"

INDICATORS = {
    "population":      {"id": "SP.POP.TOTL",        "name": "Total Population",               "unit": "Persons"},
    "pop_growth":      {"id": "SP.POP.GROW",         "name": "Population Growth Rate",         "unit": "Annual %"},
    "life_expectancy": {"id": "SP.DYN.LE00.IN",      "name": "Life Expectancy at Birth",       "unit": "Years"},
    "birth_rate":      {"id": "SP.DYN.CBRT.IN",      "name": "Birth Rate",                     "unit": "Per 1,000 people"},
    "death_rate":      {"id": "SP.DYN.CDRT.IN",      "name": "Death Rate",                     "unit": "Per 1,000 people"},
    "fertility_rate":  {"id": "SP.DYN.TFRT.IN",      "name": "Fertility Rate",                 "unit": "Births per woman"},
    "urban_pop":       {"id": "SP.URB.TOTL.IN.ZS",   "name": "Urban Population",               "unit": "% of total"},
    "pop_65plus":      {"id": "SP.POP.65UP.TO.ZS",   "name": "Population Ages 65+",            "unit": "% of total"},
    "dependency_ratio":{"id": "SP.POP.DPND",         "name": "Age Dependency Ratio",           "unit": "% of working-age population"},
}


async def fetch_wb(indicator_id: str, limit: int = 10):
    url = f"{WB_BASE_URL}/{indicator_id}"
    params = {
        "format": "json",
        "mrv": limit,
        "per_page": limit,
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params, timeout=15)
        data = res.json()

    if not data or len(data) < 2:
        return []

    records = data[1] or []
    return [
        {"year": str(r["date"]), "value": r["value"]}
        for r in records
        if r.get("value") is not None
    ]


@app.get("/")
def root():
    return {
        "api": "Japan Demographics API",
        "version": "1.0.0",
        "description": "Japan demographic statistics — population, life expectancy, birth rate, aging, and more",
        "endpoints": [
            "/summary",
            "/population",
            "/life-expectancy",
            "/birth-rate",
            "/death-rate",
            "/fertility",
            "/urban",
            "/aging",
        ],
        "source": "World Bank Open Data (data.worldbank.org)",
        "country": "Japan (JP)",
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/summary")
async def summary(limit: int = Query(default=1, ge=1, le=30)):
    """Get latest values for all key Japan demographic indicators."""
    result = {}
    for key, meta in INDICATORS.items():
        data = await fetch_wb(meta["id"], limit=limit)
        result[key] = {
            "name": meta["name"],
            "unit": meta["unit"],
            "data": data,
        }
    return {
        "country": "Japan",
        "source": "World Bank Open Data",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "indicators": result,
    }


@app.get("/population")
async def population(limit: int = Query(default=10, ge=1, le=60)):
    """Japan total population and growth rate (annual)."""
    pop_data = await fetch_wb("SP.POP.TOTL", limit)
    growth_data = await fetch_wb("SP.POP.GROW", limit)
    return {
        "indicator": "Population",
        "country": "Japan",
        "source": "World Bank",
        "frequency": "Annual",
        "total": {"unit": "Persons", "data": pop_data},
        "growth_rate": {"unit": "Annual %", "data": growth_data},
    }


@app.get("/life-expectancy")
async def life_expectancy(limit: int = Query(default=10, ge=1, le=60)):
    """Japan life expectancy at birth (years)."""
    data = await fetch_wb("SP.DYN.LE00.IN", limit)
    return {
        "indicator": "Life Expectancy at Birth",
        "unit": "Years",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "note": "Japan consistently ranks among the highest life expectancy globally",
        "data": data,
    }


@app.get("/birth-rate")
async def birth_rate(limit: int = Query(default=10, ge=1, le=60)):
    """Japan crude birth rate (per 1,000 people)."""
    data = await fetch_wb("SP.DYN.CBRT.IN", limit)
    return {
        "indicator": "Birth Rate, Crude",
        "unit": "Per 1,000 people",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "data": data,
    }


@app.get("/death-rate")
async def death_rate(limit: int = Query(default=10, ge=1, le=60)):
    """Japan crude death rate (per 1,000 people)."""
    data = await fetch_wb("SP.DYN.CDRT.IN", limit)
    return {
        "indicator": "Death Rate, Crude",
        "unit": "Per 1,000 people",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "data": data,
    }


@app.get("/fertility")
async def fertility(limit: int = Query(default=10, ge=1, le=60)):
    """Japan total fertility rate (births per woman)."""
    data = await fetch_wb("SP.DYN.TFRT.IN", limit)
    return {
        "indicator": "Fertility Rate, Total",
        "unit": "Births per woman",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "data": data,
    }


@app.get("/urban")
async def urban(limit: int = Query(default=10, ge=1, le=60)):
    """Japan urban population (% of total)."""
    data = await fetch_wb("SP.URB.TOTL.IN.ZS", limit)
    return {
        "indicator": "Urban Population",
        "unit": "% of total population",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "data": data,
    }


@app.get("/aging")
async def aging(limit: int = Query(default=10, ge=1, le=60)):
    """Japan aging population — 65+ share and dependency ratio."""
    pop65_data = await fetch_wb("SP.POP.65UP.TO.ZS", limit)
    dep_data = await fetch_wb("SP.POP.DPND", limit)
    return {
        "country": "Japan",
        "source": "World Bank",
        "frequency": "Annual",
        "note": "Japan has one of the world's oldest populations",
        "pop_65plus": {"unit": "% of total", "data": pop65_data},
        "dependency_ratio": {"unit": "% of working-age population", "data": dep_data},
    }

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path == "/":
        return await call_next(request)
    key = request.headers.get("X-RapidAPI-Key", "")
    if not key:
        return JSONResponse(status_code=401, content={"detail": "Missing X-RapidAPI-Key header"})
    return await call_next(request)
