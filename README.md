# MCP Wyze Server

An MCP (Model Context Protocol) server for controlling Wyze smart home devices using the wyze-sdk library.

## Overview

This MCP server provides a comprehensive interface for interacting with Wyze devices through AI assistants like Claude. It supports authentication, device discovery, device control, and group management for various Wyze smart home products.

## Features

- **Authentication**: Secure login using Wyze API credentials
- **Device Discovery**: List and get information about all Wyze devices
- **Device Control**: Turn devices on/off, adjust brightness, and more
- **Group Management**: Control entire rooms or groups of devices at once
- **Live Resources**: Real-time device and group status monitoring
- **Automatic Login**: Uses environment variables for seamless authentication

## Prerequisites

- Python 3.13+
- Wyze developer account with API credentials
- `uv` package manager

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
uv pip install mcp-wyze-server
```

Or with pip:
```bash
pip install mcp-wyze-server
```

### Option 2: Install from Source

1. Clone the repository:
```bash
git clone https://github.com/aldilaff/mcp-wyze-server.git
cd mcp-wyze-server
```

2. Install with uv:
```bash
uv pip install -e .
```

Or build and install:
```bash
uv build
uv pip install dist/*.whl
```

### Configure Environment Variables

After installation, configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your Wyze credentials:
```
WYZE_EMAIL=your-email@example.com
WYZE_PASSWORD=your-password
WYZE_KEY_ID=your-key-id-here
WYZE_API_KEY=your-api-key-here
```

### Getting Wyze API Credentials

To obtain your Wyze API credentials:

1. Visit the [Wyze Developer Portal](https://developer-api-console.wyze.com/)
2. Create a developer account if you don't have one
3. Create a new API key
4. Note down your `KEY_ID` and `API_KEY`

## Usage

### Running the Server Standalone

If installed from PyPI:
```bash
mcp-wyze-server
```

If running from source:
```bash
uv run python src/mcp_wyze_server/server.py
```

### Integrating with Claude Desktop

Add this configuration to your Claude Desktop MCP settings:

**If installed globally via pip/uv:**
```json
{
  "mcpServers": {
    "wyze": {
      "command": "/Users/{yourusername}/.local/bin/uv",
      "args": ["tool", "run", "mcp-wyze-server"],
      "env": {
        "WYZE_EMAIL": "your-email@example.com",
        "WYZE_PASSWORD": "your-password",
        "WYZE_KEY_ID": "your-key-id",
        "WYZE_API_KEY": "your-api-key"
      }
    }
  }
}
```

Note: Replace `/Users/yourusername/.local/bin/uv` with the actual path to your `uv` installation. You can find this by running `which uv` in your terminal.

**If running from source (recommended for development):**
```json
{
  "mcpServers": {
    "wyze": {
      "command": "/Users/yourusername/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/path/to/mcp-wyze-server",
        "python",
        "src/mcp_wyze_server/server.py"
      ],
      "env": {
        "WYZE_EMAIL": "your-email@example.com",
        "WYZE_PASSWORD": "your-password",
        "WYZE_KEY_ID": "your-key-id",
        "WYZE_API_KEY": "your-api-key"
      }
    }
  }
}
```

Note: Replace `/Users/yourusername/.local/bin/uv` with your actual `uv` path.

### Configuration with Other MCP Clients

This server uses stdio transport and can be integrated with any MCP client that supports the protocol. 

If installed via PyPI:
```bash
mcp-wyze-server
```

If running from source:
```bash
uv run python /path/to/mcp-wyze-server/src/mcp_wyze_server/server.py
```

## Available MCP Tools

### Authentication
- `wyze_login()` - Login to Wyze account (uses env vars)

### Device Management
- `wyze_get_devices()` - List all devices
- `wyze_device_info(device_mac)` - Get device details
- `wyze_get_device_status(device_mac)` - Get accurate current status (power state, brightness, etc.)

### Basic Device Control
- `wyze_turn_on_device(device_mac)` - Turn on a device
- `wyze_turn_off_device(device_mac)` - Turn off a device
- `wyze_set_brightness(device_mac, brightness)` - Set brightness (0-100)

### Enhanced Light Control
- `wyze_set_color_temp(device_mac, color_temp)` - Set color temperature (2700K-6500K)
- `wyze_set_color(device_mac, color)` - Set RGB color (hex format)
- `wyze_set_light_effect(device_mac, effect)` - Set visual effects
- `wyze_set_light_sun_match(device_mac, enabled)` - Enable/disable sun matching
- `wyze_clear_light_timer(device_mac)` - Clear scheduled timers

### Scale Management
- `wyze_get_scales()` - List all Wyze scales
- `wyze_get_scale_info(device_mac)` - Get detailed scale information  
- `wyze_get_scale_records(device_mac, user_id, days_back)` - Get weight/body composition records

### Resources
- `wyze://devices` - Live device list with status
- `wyze://scales` - Live scale list with family members

### Prompts
- `wyze_device_control_prompt(device_name, action)` - Generate control prompts
- `wyze_scale_health_prompt(family_member_name, timeframe)` - Generate health analysis prompts

## Supported Devices

This server supports various Wyze device types including:
- Lights (Bulbs, Light Strips)
- Switches
- Plugs
- Scales
- Locks
- Cameras (basic control)
- Thermostats
- And more...

## Development

This project uses:
- **FastMCP**: A high-performance MCP server framework
- **wyze-sdk**: Comprehensive Python interface for Wyze devices
- **uv**: Fast Python package manager

### Project Structure

```
mcp-wyze-server/
├── src/
│   └── mcp_wyze_server/
│       ├── __init__.py
│       └── server.py     # MCP server implementation
├── test_device.py        # Device testing utility
├── pyproject.toml        # Project dependencies
├── .env.example          # Environment variables template
├── CLAUDE.md             # Development guidelines for Claude
├── LICENSE               # MIT License
└── README.md             # This file
```

## Troubleshooting

### Common Issues

1. **Authentication Failed**: Ensure your Wyze credentials are correct and API keys are valid
2. **Device Not Found**: Device MAC addresses are case-sensitive
3. **Connection Timeout**: Check your network connection and Wyze service status

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
export MCP_DEBUG=true
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Wyze SDK](https://github.com/shauntarves/wyze-sdk) for the excellent Python library
- [MCP](https://modelcontextprotocol.io/) for the Model Context Protocol specification
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server framework

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by Wyze Labs, Inc. All product names, logos, and brands are property of their respective owners.