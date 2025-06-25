# Kafka Data Flow Demos with Docker

This project provides three simple, self-contained demonstrations of common data flow patterns using Python and Apache Kafka, all running within Docker containers.

- **Publish/Subscribe (Pub/Sub):** A basic demonstration of a producer sending messages and a consumer receiving them in real-time.
- **Batch Processing:** A demo where a large number of messages are produced, and a separate process reads them all in a single batch, performs an aggregation, and then exits.
- **Stream Processing:** A real-time demonstration where a continuous stream of data is processed using a "tumbling window" to calculate an average over a fixed time interval.

## Prerequisites

- Docker
- Docker Compose

You do not need to install Python or Kafka on your local machine; everything is containerized.

## How to Run the Demos

You must run each demo from its respective directory (`pub-sub`, `batch`, or `stream`).

---
