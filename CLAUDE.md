# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server for controlling Wyze smart home devices using the wyze-sdk library. The server provides tools for authentication, device discovery, and device control through the MCP protocol.

## Key Architecture

- **src/mcp_wyze_server/server.py**: MCP server implementation using FastMCP framework with Wyze device integration
- **FastMCP Framework**: Uses decorators to define tools (`@mcp.tool()`), resources (`@mcp.resource()`), and prompts (`@mcp.prompt()`)
- **Wyze Integration**: Uses wyze-sdk library for communication with Wyze devices
- **Global Client**: Maintains a single Wyze client instance for efficient API usage

## Development Commands

### Environment Setup

Set environment variables for Wyze credentials (required):

```bash
export WYZE_EMAIL="your-email@example.com"
export WYZE_PASSWORD="your-password"
export WYZE_KEY_ID="your-key-id"
export WYZE_API_KEY="your-api-key"
```

### Running the Server

From the project directory:
```bash
uv run python src/mcp_wyze_server/server.py
```

Or using the package entry point after installation:
```bash
mcp-wyze-server
```

### Package Management

This project uses `uv` for dependency management:

- Dependencies are defined in `pyproject.toml`
- Lock file: `uv.lock`
- Main dependencies: `mcp[cli]>=1.12.2`, `wyze-sdk>=1.10.0`

### Installing Dependencies

```bash
uv sync
```

## MCP Tools Available

### Authentication

- `wyze_login()`: Login to Wyze account using environment variables (no parameters)
- Auto-login: Server automatically attempts login using credentials on first API call

### Device Management

- `wyze_get_devices()`: List all devices in the account
- `wyze_device_info(device_mac)`: Get detailed info for a specific device
- `wyze_get_device_status(device_mac)`: Get accurate current status (power state, brightness, color, etc.)

### Basic Device Control

- `wyze_turn_on_device(device_mac)`: Turn on a device
- `wyze_turn_off_device(device_mac)`: Turn off a device
- `wyze_set_brightness(device_mac, brightness)`: Set brightness (0-100) for lights


### Enhanced Light Control

- `wyze_set_color_temp(device_mac, color_temp)`: Set color temperature (2700K-6500K)
- `wyze_set_color(device_mac, color)`: Set RGB color (hex format like 'ff0000')
- `wyze_set_light_effect(device_mac, effect)`: Set visual effects for light strips
- `wyze_set_light_sun_match(device_mac, enabled)`: Enable/disable sun matching
- `wyze_clear_light_timer(device_mac)`: Clear scheduled timers


### Scale Management

- `wyze_get_scales()`: List all Wyze scales in the account
- `wyze_get_scale_info(device_mac)`: Get detailed information about a specific scale
- `wyze_get_scale_records(device_mac, user_id, days_back)`: Get weight and body composition records

### Resources

- `wyze://devices`: Live list of all Wyze devices with status
- `wyze://scales`: Live list of scales with family members

### Prompts

- `wyze_device_control_prompt(device_name, action)`: Generate control prompts
- `wyze_scale_health_prompt(family_member_name, timeframe)`: Generate health analysis prompts

## Error Handling

All tools return structured responses with `status` field ("success" or "error") and appropriate `message` or data fields. The server handles `WyzeAPIError` exceptions specifically.

## Claude Development Rules

### Library Research Priority

When researching the wyze-sdk library or other Python dependencies:

1. **FIRST**: Search local code in `.venv/lib/python*/site-packages/wyze_sdk/` using Glob, Grep, and Read tools
2. **EXAMINE**: Check the library's source code, types, services, and API methods locally
3. **AVOID**: Web searches for library documentation unless local code examination is insufficient
4. **RATIONALE**: Local code provides the most accurate, current implementation details

This ensures development decisions are based on the actual installed library version rather than potentially outdated web documentation.
