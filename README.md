# JuniorOmega

**Sovereign Spatial Computing & Fabrication SDK**

JuniorOmega is the spatial engineering layer of the JuniorCloud LLC stack. It bridges high-density sensor ingestion (LiDAR, TrueDepth, multi-camera) with automated fabrication pipelines (G-code, CNC, robotic control).

It works closely with crispy-mouse for low-level sensing and execution, and feeds spatial state into BitNet-mlx reasoning pipelines.

## Core Responsibilities

- Multi-modal spatial data ingestion (optical + depth)
- Point cloud and mesh processing optimized for Apple Silicon
- G-code and fabrication pipeline generation
- Integration with room-scale sensing systems (JuniorClimbs direction)

## Ecosystem Position

| Component        | Interaction with JuniorOmega                     |
|------------------|--------------------------------------------------|
| **crispy-mouse** | Low-level sensor input and execution             |
| **BitNet-mlx**   | Spatial state → reasoning                       |
| **JuniorClimbs** | Shares multi-optical room mapping vision         |
| **JuniorHome**   | Central orchestration                            |

JuniorOmega is designed as a production-grade, sovereign spatial computing foundation for both performance analytics and physical fabrication use cases.