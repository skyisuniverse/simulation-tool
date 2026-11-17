# MCP

From conversation with Geminin on [Model Context Protocol (MCP)](https://share.google/aimode/wnz136NDG6Yfo428b)

The **Model Context Protocol (MCP)** is an open-source standard introduced by Anthropic that acts like a "USB-C port for AI applications". It standardizes how AI models and agents connect to external data sources, tools, and workflows. You can explore the official standard and tools via the [Model Context Protocol Website](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro).

## Core Architecture

MCP uses a client-server model to separate the AI application from the underlying tools:

- **MCP Host**: The AI-powered application or environment (such as Claude Desktop, VS Code, or Cursor) where the LLM runs and user interactions happen.

- **MCP Client**: A component inside the host that maintains connections to MCP servers and translates requests back and forth.

- **MCP Server**: A lightweight program that exposes specific data sources, documents, databases, or tools (like GitHub, Google Drive, or Postgres) to the client using a standardized schema.

## Why MCP Matters

- **Universal Connection**: Instead of developers writing custom integrations for every single AI model and tool combination, you build one MCP server per tool, and any MCP-compatible AI app can use it.

- **Dynamic Tool Discovery**: The client asks the server what tools and data resources are available, and the server returns natural-language descriptions and schemas that the LLM can call on the fly.

- **Enhanced Security**: Credentials and API keys stay isolated inside the MCP server rather than being exposed directly inside the client prompt.

## Supported SDKs & Ecosystem

MCP is hosted as an open-source project under the Linux Foundation and offers official software development kits (SDKs) across multiple languages:

- Python SDK (`modelcontextprotocol/python-sdk`)
- TypeScript SDK
- Java SDK (`modelcontextprotocol/java-sdk`)
- Go SDK (`modelcontextprotocol/go-sdk`)
- Kotlin & Rust SDKs (`modelcontextprotocol/rust-sdk`, `modelcontextprotocol/kotlin-sdk`)

Are you looking to:

- **build a custom MCP server**, 
- or do you want to **connect existing MCP servers** to an AI tool like Claude, Cursor, or VS Code?

---


[Model Context Protocol (Wikipedia)](https://en.wikipedia.org/wiki/Model_Context_Protocol)
