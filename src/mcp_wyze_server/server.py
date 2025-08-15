"""
MCP Server for Wyze devices using wyze-sdk library.

Run with:
    uv run python main.py
"""

import os
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP
from wyze_sdk import Client
from wyze_sdk.errors import WyzeClientConfigurationError, WyzeRequestError

# Create an MCP server
mcp = FastMCP("Wyze")

# Global client instance
_wyze_client: Optional[Client] = None


def get_wyze_client() -> Client:
    """Get or create Wyze client instance with auto-login if credentials available"""
    global _wyze_client
    
    if _wyze_client is None:
        # Get credentials from environment
        email = os.getenv("WYZE_EMAIL")
        password = os.getenv("WYZE_PASSWORD")
        key_id = os.getenv("WYZE_KEY_ID")
        api_key = os.getenv("WYZE_API_KEY")
        
        if not all([email, password, key_id, api_key]):
            raise WyzeClientConfigurationError(
                "Missing required environment variables: WYZE_EMAIL, WYZE_PASSWORD, WYZE_KEY_ID, WYZE_API_KEY"
            )
        
        _wyze_client = Client(
            email=email,
            password=password,
            key_id=key_id,
            api_key=api_key
        )
    
    return _wyze_client


@mcp.tool()
def wyze_login() -> Dict[str, str]:
    """Login to Wyze account using environment variables"""
    try:
        client = get_wyze_client()
        return {"status": "success", "message": "Successfully logged in to Wyze"}
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_get_devices() -> Dict[str, Any]:
    """Get list of all Wyze devices associated with the account"""
    try:
        client = get_wyze_client()
        devices = client.devices_list()
        
        device_list = []
        for device in devices:
            device_info = {
                "mac": str(device.mac) if device.mac else "Unknown",
                "nickname": str(device.nickname) if device.nickname else "Unknown",
                "product_model": str(getattr(device, 'product_model', 'Unknown')) if getattr(device, 'product_model', 'Unknown') else "Unknown",
                "product_type": str(getattr(device, 'product_type', 'Unknown')) if getattr(device, 'product_type', 'Unknown') else "Unknown",
                "is_online": bool(getattr(device, 'is_online', True)),
                "firmware_ver": str(getattr(device, 'firmware_ver', 'N/A')),
            }
            device_list.append(device_info)
        
        return {
            "status": "success",
            "devices": device_list,
            "count": len(device_list)
        }
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_device_info(device_mac: str) -> Dict[str, Any]:
    """Get detailed information about a specific Wyze device by MAC address"""
    try:
        client = get_wyze_client()
        devices = client.devices_list()
        
        for device in devices:
            if device.mac == device_mac:
                device_info = {
                    "mac": str(device.mac) if device.mac else "Unknown",
                    "nickname": str(device.nickname) if device.nickname else "Unknown",
                    "product_model": str(getattr(device, 'product_model', 'Unknown')) if getattr(device, 'product_model', 'Unknown') else "Unknown",
                    "product_type": str(getattr(device, 'product_type', 'Unknown')) if getattr(device, 'product_type', 'Unknown') else "Unknown",
                    "is_online": bool(getattr(device, 'is_online', True)),
                    "firmware_ver": str(getattr(device, 'firmware_ver', 'N/A')),
                    "device_model": str(getattr(device, 'device_model', 'Unknown')),
                }
                return {"status": "success", "device": device_info}
        
        return {"status": "error", "message": f"Device with MAC {device_mac} not found"}
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_turn_on_device(device_mac: str) -> Dict[str, str]:
    """Turn on a Wyze light device"""
    try:
        client = get_wyze_client()
        devices = client.devices_list()
        
        for device in devices:
            if device.mac == device_mac:
                # Get device type - try multiple approaches
                device_type = (getattr(device, 'product_type', None) or 
                              getattr(device, 'type', None) or
                              (hasattr(device, 'product') and getattr(device.product, 'type', None)) or
                              'Unknown')
                
                device_model = (getattr(device, 'product_model', None) or
                               getattr(device, 'model', None) or
                               (hasattr(device, 'product') and getattr(device.product, 'model', None)) or
                               'Unknown')
                
                if device_type in ['Light', 'Bulb', 'MeshLight', 'LightStrip']:
                    client.bulbs.turn_on(device_mac=device_mac, device_model=device_model)
                else:
                    return {"status": "error", "message": f"Device type '{device_type}' is not a supported light device"}
                
                return {"status": "success", "message": f"Device {device.nickname} turned on"}
        
        return {"status": "error", "message": f"Device with MAC {device_mac} not found"}
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_turn_off_device(device_mac: str) -> Dict[str, str]:
    """Turn off a Wyze light device"""
    try:
        client = get_wyze_client()
        devices = client.devices_list()
        
        for device in devices:
            if device.mac == device_mac:
                # Get device type - try multiple approaches
                device_type = (getattr(device, 'product_type', None) or 
                              getattr(device, 'type', None) or
                              (hasattr(device, 'product') and getattr(device.product, 'type', None)) or
                              'Unknown')
                
                device_model = (getattr(device, 'product_model', None) or
                               getattr(device, 'model', None) or
                               (hasattr(device, 'product') and getattr(device.product, 'model', None)) or
                               'Unknown')
                
                if device_type in ['Light', 'Bulb', 'MeshLight', 'LightStrip']:
                    client.bulbs.turn_off(device_mac=device_mac, device_model=device_model)
                else:
                    return {"status": "error", "message": f"Device type '{device_type}' is not a supported light device"}
                
                return {"status": "success", "message": f"Device {device.nickname} turned off"}
        
        return {"status": "error", "message": f"Device with MAC {device_mac} not found"}
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_set_brightness(device_mac: str, brightness: int) -> Dict[str, str]:
    """Set brightness for a Wyze light (0-100)"""
    try:
        if not 0 <= brightness <= 100:
            return {"status": "error", "message": "Brightness must be between 0 and 100"}
        
        client = get_wyze_client()
        devices = client.devices_list()
        
        for device in devices:
            if device.mac == device_mac:
                # Get device type - try multiple approaches
                device_type = (getattr(device, 'product_type', None) or 
                              getattr(device, 'type', None) or
                              (hasattr(device, 'product') and getattr(device.product, 'type', None)) or
                              'Unknown')
                
                device_model = (getattr(device, 'product_model', None) or
                               getattr(device, 'model', None) or
                               (hasattr(device, 'product') and getattr(device.product, 'model', None)) or
                               'Unknown')
                
                if device_type in ['Light', 'Bulb', 'MeshLight', 'LightStrip']:
                    client.bulbs.set_brightness(
                        device_mac=device_mac, 
                        device_model=device_model, 
                        brightness=brightness
                    )
                    return {"status": "success", "message": f"Set {device.nickname} brightness to {brightness}%"}
                else:
                    return {"status": "error", "message": f"Device {device.nickname} does not support brightness control"}
        
        return {"status": "error", "message": f"Device with MAC {device_mac} not found"}
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_get_scales() -> Dict[str, Any]:
    """Get list of all Wyze scales associated with the account"""
    try:
        client = get_wyze_client()
        scales = client.scales.list()
        
        scale_list = []
        for scale in scales:
            scale_info = {
                "mac": str(scale.mac) if scale.mac else "Unknown",
                "nickname": str(scale.nickname) if scale.nickname else "Unknown",
                "product_model": str(getattr(scale, 'product_model', 'Unknown')) if getattr(scale, 'product_model', 'Unknown') else "Unknown",
                "product_type": str(getattr(scale, 'product_type', 'Scale')) if getattr(scale, 'product_type', 'Scale') else "Scale",
                "is_online": bool(getattr(scale, 'is_online', True)),
                "firmware_ver": str(getattr(scale, 'firmware_ver', 'N/A')),
            }
            scale_list.append(scale_info)
        
        return {
            "status": "success",
            "scales": scale_list,
            "count": len(scale_list)
        }
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_get_scale_info(device_mac: str) -> Dict[str, Any]:
    """Get detailed information about a specific Wyze scale"""
    try:
        client = get_wyze_client()
        scale = client.scales.info(device_mac=device_mac)
        
        if scale is None:
            return {"status": "error", "message": f"Scale with MAC {device_mac} not found"}
        
        scale_info = {
            "mac": str(scale.mac) if scale.mac else "Unknown",
            "nickname": str(scale.nickname) if scale.nickname else "Unknown",
            "product_model": str(getattr(scale, 'product_model', 'Unknown')) if getattr(scale, 'product_model', 'Unknown') else "Unknown",
            "product_type": str(getattr(scale, 'product_type', 'Scale')) if getattr(scale, 'product_type', 'Scale') else "Scale",
            "is_online": bool(getattr(scale, 'is_online', True)),
            "firmware_ver": str(getattr(scale, 'firmware_ver', 'N/A')),
        }
        
        # Add family members if available
        if hasattr(scale, 'family_members') and scale.family_members:
            family_members = []
            for member in scale.family_members:
                member_info = {
                    "id": str(member.get("id", "Unknown")),
                    "nickname": str(member.get("nickname", "Unknown")),
                    "height": float(member.get("height")) if member.get("height") is not None else None,
                    "goal_weight": float(member.get("goal_weight")) if member.get("goal_weight") is not None else None,
                }
                family_members.append(member_info)
            scale_info["family_members"] = family_members
        
        return {"status": "success", "scale": scale_info}
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_get_scale_records(
    device_mac: str = None,
    user_id: str = None,
    days_back: int = 30
) -> Dict[str, Any]:
    """Get weight measurement records from a Wyze scale"""
    try:
        from datetime import datetime, timedelta
        
        client = get_wyze_client()
        
        # Calculate time range
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days_back)
        
        records = client.scales.get_records(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time
        )
        
        record_list = []
        for record in records:
            record_info = {
                "measure_time": int(record.measure_ts) if hasattr(record, 'measure_ts') and record.measure_ts else None,
                "weight": float(record.weight) if hasattr(record, 'weight') and record.weight is not None else None,
                "bmi": float(record.bmi) if hasattr(record, 'bmi') and record.bmi is not None else None,
                "body_fat": float(record.body_fat) if hasattr(record, 'body_fat') and record.body_fat is not None else None,
                "muscle_mass": float(record.muscle) if hasattr(record, 'muscle') and record.muscle is not None else None,
                "heart_rate": int(record.heart_rate) if hasattr(record, 'heart_rate') and record.heart_rate is not None else None,
            }
            record_list.append(record_info)
        
        return {
            "status": "success",
            "records": record_list,
            "count": len(record_list),
            "days_back": days_back
        }
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_get_device_status(device_mac: str) -> Dict[str, Any]:
    """Get accurate current status for a Wyze device (power state, brightness, etc.)"""
    try:
        client = get_wyze_client()
        devices = client.devices_list()
        
        # Find the device first
        target_device = None
        for device in devices:
            if device.mac == device_mac:
                target_device = device
                break
        
        if not target_device:
            return {"status": "error", "message": f"Device with MAC {device_mac} not found"}
        
        device_type = getattr(target_device, 'product_type', 'Unknown')
        device_status = {
            "mac": device_mac,
            "nickname": target_device.nickname,
            "product_type": device_type,
            "product_model": getattr(target_device, 'product_model', 'Unknown'),
        }
        
        # Get detailed status based on device type
        if device_type in ['Light', 'Bulb', 'MeshLight', 'LightStrip']:
            try:
                detailed_device = client.bulbs.info(device_mac=device_mac)
                if detailed_device:
                    device_status.update({
                        "is_on": getattr(detailed_device, 'is_on', None),
                        "brightness": getattr(detailed_device, 'brightness', None),
                        "color_temp": getattr(detailed_device, 'color_temp', None),
                        "color": getattr(detailed_device, 'color', None),
                    })
                else:
                    device_status["error"] = "Could not retrieve detailed bulb information"
            except Exception as e:
                device_status["error"] = f"Error getting bulb status: {str(e)}"
                
        else:
            # For other device types, show basic online status
            device_status["is_online"] = getattr(target_device, 'is_online', None)
        
        return {"status": "success", "device_status": device_status}
        
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


# Enhanced Light Control Functions

@mcp.tool()
def wyze_set_color_temp(device_mac: str, color_temp: int) -> Dict[str, str]:
    """Set color temperature for a Wyze light (2700K-6500K)"""
    try:
        if not 2700 <= color_temp <= 6500:
            return {"status": "error", "message": "Color temperature must be between 2700K and 6500K"}
        
        client = get_wyze_client()
        devices = client.devices_list()
        
        for device in devices:
            if device.mac == device_mac and getattr(device, 'product_type', 'Unknown') in ['Light', 'Bulb', 'MeshLight', 'LightStrip']:
                client.bulbs.set_color_temp(
                    device_mac=device_mac,
                    device_model=getattr(device, 'product_model', 'Unknown'),
                    color_temp=color_temp
                )
                return {"status": "success", "message": f"Set {device.nickname} color temperature to {color_temp}K"}
        
        return {"status": "error", "message": f"Light with MAC {device_mac} not found"}
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_set_color(device_mac: str, color: str) -> Dict[str, str]:
    """Set RGB color for a Wyze light (hex format like 'ff0000' for red)"""
    try:
        # Validate hex color format
        if not color.startswith('#'):
            color = '#' + color
        if len(color) != 7 or not all(c in '0123456789abcdefABCDEF' for c in color[1:]):
            return {"status": "error", "message": "Color must be in hex format (e.g., 'ff0000' or '#ff0000')"}
        
        client = get_wyze_client()
        devices = client.devices_list()
        
        for device in devices:
            if device.mac == device_mac:
                # Get device type from multiple possible attributes
                device_type = (getattr(device, 'product_type', None) or 
                              getattr(device, 'type', None) or
                              (hasattr(device, 'product') and getattr(device.product, 'type', None)) or
                              'Unknown')
                
                device_model = (getattr(device, 'product_model', None) or
                               (hasattr(device, 'product') and getattr(device.product, 'model', None)) or
                               'Unknown')
                
                if device_type in ['Light', 'Bulb', 'MeshLight', 'LightStrip']:
                    client.bulbs.set_color(
                        device_mac=device_mac,
                        device_model=device_model,
                        color=color
                    )
                    return {"status": "success", "message": f"Set {device.nickname} color to {color}"}
        
        return {"status": "error", "message": f"Light with MAC {device_mac} not found"}
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_set_light_effect(device_mac: str, effect: str) -> Dict[str, str]:
    """Set visual effect for a Wyze light strip or compatible bulb"""
    try:
        client = get_wyze_client()
        devices = client.devices_list()
        
        for device in devices:
            if device.mac == device_mac and getattr(device, 'product_type', 'Unknown') in ['Light', 'Bulb', 'MeshLight', 'LightStrip']:
                client.bulbs.set_effect(
                    device_mac=device_mac,
                    device_model=getattr(device, 'product_model', 'Unknown'),
                    effect=effect
                )
                return {"status": "success", "message": f"Set {device.nickname} effect to {effect}"}
        
        return {"status": "error", "message": f"Light with MAC {device_mac} not found"}
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_set_light_sun_match(device_mac: str, enabled: bool = True) -> Dict[str, str]:
    """Enable or disable sun matching for a Wyze light (adjusts color temperature based on time of day)"""
    try:
        client = get_wyze_client()
        devices = client.devices_list()
        
        for device in devices:
            if device.mac == device_mac and getattr(device, 'product_type', 'Unknown') in ['Light', 'Bulb', 'MeshLight', 'LightStrip']:
                client.bulbs.set_sun_match(
                    device_mac=device_mac,
                    device_model=getattr(device, 'product_model', 'Unknown'),
                    sun_match=enabled
                )
                status = "enabled" if enabled else "disabled"
                return {"status": "success", "message": f"Sun matching {status} for {device.nickname}"}
        
        return {"status": "error", "message": f"Light with MAC {device_mac} not found"}
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def wyze_clear_light_timer(device_mac: str) -> Dict[str, str]:
    """Clear any scheduled timers for a Wyze light"""
    try:
        client = get_wyze_client()
        devices = client.devices_list()
        
        for device in devices:
            if device.mac == device_mac and getattr(device, 'product_type', 'Unknown') in ['Light', 'Bulb', 'MeshLight', 'LightStrip']:
                client.bulbs.clear_timer(
                    device_mac=device_mac,
                    device_model=getattr(device, 'product_model', 'Unknown')
                )
                return {"status": "success", "message": f"Cleared timer for {device.nickname}"}
        
        return {"status": "error", "message": f"Light with MAC {device_mac} not found"}
    except WyzeClientConfigurationError as e:
        return {"status": "error", "message": f"Configuration error: {str(e)}"}
    except WyzeRequestError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.resource("wyze://devices")
def get_devices_resource() -> str:
    """Resource providing current list of Wyze light devices with accurate status"""
    try:
        client = get_wyze_client()
        devices = client.devices_list()
        
        device_summary = "Wyze Devices:\n\n"
        for device in devices:
            # Get device type - try multiple approaches
            device_type = (getattr(device, 'product_type', None) or 
                          getattr(device, 'type', None) or
                          (hasattr(device, 'product') and getattr(device.product, 'type', None)) or
                          'Unknown')
            
            # Get accurate device status based on type
            if device_type in ['Light', 'Bulb', 'MeshLight', 'LightStrip']:
                try:
                    detailed_device = client.bulbs.info(device_mac=device.mac)
                    if detailed_device and hasattr(detailed_device, 'is_on'):
                        power_status = "💡 On" if detailed_device.is_on else "🌙 Off"
                    else:
                        power_status = "❓ Unknown"
                except:
                    power_status = "❓ Unknown"
            else:
                # For other devices, show online/offline status
                power_status = "🟢 Online" if getattr(device, 'is_online', True) else "🔴 Offline"
            
            device_summary += f"• {device.nickname} ({getattr(device, 'product_model', 'Unknown')}) - {power_status}\n"
            device_summary += f"  MAC: {device.mac}\n"
            device_summary += f"  Type: {device_type}\n\n"
        
        return device_summary
    except Exception as e:
        return f"Error retrieving devices: {str(e)}"


@mcp.resource("wyze://scales")
def get_scales_resource() -> str:
    """Resource providing current list of Wyze scales"""
    try:
        client = get_wyze_client()
        scales = client.scales.list()
        
        scales_summary = "Wyze Scales:\n\n"
        
        for scale in scales:
            status = "🟢 Online" if getattr(scale, 'is_online', True) else "🔴 Offline"
            scales_summary += f"⚖️ {scale.nickname} ({getattr(scale, 'product_model', 'Unknown')}) - {status}\n"
            scales_summary += f"  MAC: {scale.mac}\n"
            
            # Try to get detailed info with family members
            try:
                detailed_scale = client.scales.info(device_mac=scale.mac)
                if detailed_scale and hasattr(detailed_scale, 'family_members') and detailed_scale.family_members:
                    scales_summary += "  Family Members:\n"
                    for member in detailed_scale.family_members:
                        scales_summary += f"    • {member.get('nickname', 'Unknown')} (ID: {member.get('id')})\n"
                else:
                    scales_summary += "  Family Members: None registered\n"
            except Exception:
                scales_summary += "  Family Members: Unable to retrieve\n"
            
            scales_summary += "\n"
        
        if not scales:
            scales_summary += "No scales found in your account.\n"
        
        return scales_summary
    except Exception as e:
        return f"Error retrieving scales: {str(e)}"


@mcp.prompt()
def wyze_device_control_prompt(device_name: str, action: str) -> str:
    """Generate a prompt for controlling a Wyze device"""
    return f"""Please help me control my Wyze device "{device_name}" by performing the action: {action}.

If this requires specific device capabilities or parameters, please ask for clarification.
Common actions include:
- Turn on/off
- Set brightness (0-100)
- Set color temperature (2700K-6500K)
- Set color (hex format)
- Check status"""


@mcp.prompt()
def wyze_scale_health_prompt(family_member_name: str, timeframe: str = "last week") -> str:
    """Generate a prompt for analyzing scale health data"""
    return f"""Please help me analyze the health data for "{family_member_name}" from my Wyze scale over the {timeframe}.

I'd like to understand:
- Weight trends and changes
- Body composition changes (BMI, body fat, muscle mass)
- Heart rate patterns if available
- Any notable health indicators

Please provide insights and recommendations based on the data."""


def main():
    """Entry point for the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()