# Japan Demographics API

Real-time Japan demographic statistics powered by **World Bank Open Data**.

**Live API**: https://japan-demographics-api.vercel.app
**RapidAPI**: [Japan Demographics API](https://rapidapi.com/193market/api/japan-demographics-api)

---

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info & endpoint list |
| `GET /summary` | All indicators (latest snapshot) |
| `GET /population` | Total population & growth rate |
| `GET /life-expectancy` | Life expectancy at birth (years) |
| `GET /birth-rate` | Crude birth rate (per 1,000) |
| `GET /death-rate` | Crude death rate (per 1,000) |
| `GET /fertility` | Total fertility rate |
| `GET /urban` | Urban population (% of total) |
| `GET /aging` | Population 65+ & dependency ratio |

All endpoints accept `?limit=N` (default 10, max 60).

---

## Example

```bash
curl https://japan-demographics-api.vercel.app/life-expectancy?limit=5
```

---

## Data Source

- **Provider**: World Bank Open Data (data.worldbank.org)
- **License**: Creative Commons Attribution 4.0 (CC BY 4.0)
- **Update frequency**: Annual
- **No API key required**

---

## Pricing (RapidAPI)

| Plan | Requests/month | Price |
|------|---------------|-------|
| BASIC | 500,000 | Free |
| PRO | Unlimited | $9/month |
| ULTRA | Unlimited | $29/month |

---

## By GlobalData Store

- GitHub: [193market](https://github.com/193market)
- Email: 193market@gmail.com
