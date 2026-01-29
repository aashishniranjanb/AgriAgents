# AgriAgents Documentation

Complete documentation for the AgriAgents multi-agent irrigation AI system.

---

## Documentation Index

| Document | Description |
|----------|-------------|
| [Getting Started](./getting_started.md) | Quick start, installation, and setup |
| [Architecture](./architecture.md) | System overview and data flow |
| [Agents](./agents.md) | Detailed agent specifications |
| [API Reference](./api.md) | REST API endpoints |
| [Firmware](./firmware.md) | ESP32 firmware documentation |
| [Demo Guide](./demo_guide.md) | Demo scenarios and talking points |

---

## Quick Links

### Start Here
- **New to AgriAgents?** → [Getting Started](./getting_started.md)
- **Understanding the system?** → [Architecture](./architecture.md)

### Development
- **Building integrations?** → [API Reference](./api.md)
- **Hardware setup?** → [Firmware](./firmware.md)

### Demos & Presentations
- **Preparing a demo?** → [Demo Guide](./demo_guide.md)
- **Explaining agents?** → [Agents](./agents.md)

---

## Project Overview

AgriAgents is a multi-agent AI system for climate-aware irrigation that:

1. **Edge Processing** — ESP32 handles safety-critical decisions
2. **Multi-Agent Reasoning** — 4 specialized agents collaborate
3. **Climate Awareness** — Weather predictions override local decisions
4. **Explainable AI** — All decisions are transparent and traceable
5. **Impact Quantification** — Water savings and efficiency metrics

---

## Architecture Summary

```
ESP32 (Edge) → Backend (Agents) → Dashboard (UI)
     ↑              ↓                   ↓
  Sensors     Decision Engine     Visualization
```

**Agents:**
- 🟫 Field Agent — Sensor interpretation
- 🌦️ Climate Agent — Weather reasoning
- 🧠 Decision Agent — Utility-based decisions
- 🧑‍🌾 Farmer Assistant — Human explanations

---

## License

MIT License - See [LICENSE](../LICENSE) for details.

---

## Contact

For questions or contributions, open an issue on GitHub.
