import json
import sys
from datetime import datetime

# Function to format headers
def format_headers(headers):
    """
    Formats the headers from Flipper JSON into a list of dictionaries.
    Each dictionary contains the 'name' and 'value' of a header.
    """
    formatted_headers = []

    if headers:
        for header in headers:
            formatted_header = {
                "name": header.get("key"),
                "value": header.get("value")
            }
            formatted_headers.append(formatted_header)

    return formatted_headers


# Function to format json string into an indented and parsed version
def format_json_text(text):
    """
    Formats the response text. If the text can be parsed as JSON,
    it is formatted with indentation. Otherwise, the original text is returned.
    """
    try:
        parsed_json = json.loads(text)
        formatted_json = json.dumps(parsed_json, indent=4)
        return formatted_json
    except json.JSONDecodeError:
        # Return the original text if it cannot be parsed as JSON
        return text


# Function to get MIME type from response headers
def get_mime_type(headers):
    """
    Retrieves the 'Content-Type' MIME type from the response headers.
    If 'Content-Type' header is not present, returns 'text/plain' as default.
    """
    if headers:
        for header in headers:
            key = header.get("key"),
            value = header.get("value")

            if "Content-Type" in key:
                return value
            
    return "text/plain"  # Default value if 'Content-Type' is not present


# Function to convert Flipper JSON to HAR
def convert_flipper_to_har(flipper_data):
    """
    Converts Flipper JSON data into the HAR format.
    Returns the HAR data as a dictionary.
    """
    har_data = {
        "log": {
            "version": "1.2",
            "creator": {
                "name": "Flipper to HAR Converter",
                "version": "1.0"
            },
            "entries": []
        }
    }

    # Extract network data from Flipper JSON
    plugin_states = list(flipper_data.get("pluginStates2", {}).values())
    first_plugin_state = plugin_states[0]
    network_data = first_plugin_state.get('Network', {})
    requests = network_data.get('requests2', [])

    # Process each request in the Flipper JSON
    for request in requests:
        if not isinstance(request, dict):
            continue
        
        url = request.get("url", "")
        if not url:  # Ignore elements with empty URLs
            continue
        
        request_time = request.get("requestTime")
        response_time = request.get("responseTime")
        started_datetime = datetime.fromtimestamp(request_time / 1000.0).isoformat() + "Z"
        
        response_data = request.get("responseData", "")
        response_text = json.dumps(response_data)
        
        if request_time is not None and response_time is not None:
            duration = response_time - request_time
        else:
            duration = 0
        
        mime_type = get_mime_type(request.get("responseHeaders"))

        if "application/json" in mime_type:
            response_text = format_json_text(response_data)

        if "image/" in mime_type:
            response_text = response_text.replace('[\"', '')
            response_text = response_text.replace('\"]', '')
            encoding = "base64"
        else:
            encoding = None

        # Check if the status is "..."
        if request.get("status") == "...":
            # If status is "...", set the response object to an empty dictionary
            response = {}
        else:
            # Otherwise, populate the response object as usual
            response = {
                "status": request.get("status", 0),
                "statusText": request.get("reason", ""),
                "headers": format_headers(request.get("responseHeaders")),
                "content": {
                    "size": request.get("responseLength", 0),
                    "mimeType": mime_type,
                    "text": response_text,
                },
                "redirectURL": "",
            }

            if encoding == "base64":  # adds encoding property if needed
                response["content"]["encoding"] = encoding

        request_data = {
            "startedDateTime": started_datetime,
            "time": duration,
            "request": {
                "method": request.get("method", ""),
                "url": request.get("url", ""),
                "headers": format_headers(request.get("requestHeaders")),
            },
            "response": response,  # Use the constructed response object
            "cache": {},
            "timings": {
                "send": 0,  # not known in Flipper files so set to default values
                "wait": duration,
                "receive": 0  # not known in Flipper files so set to default values
            }
        }

        request_mime_type = get_mime_type(request.get("requestHeaders"))
        request_request_data = request.get("requestData")
        if request_request_data is not None and request_mime_type is not None and request_mime_type != "application/msgpack":
            request_data_text = format_json_text(request_request_data)
            request_data["request"]["postData"] = {
                "mimeType": request_mime_type,
                "text": request_data_text
            }

        har_data["log"]["entries"].append(request_data)

    return har_data


# Entry point of the script
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python myScript.py input.json output.har")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        # Read Flipper JSON from input file
        with open(input_file, "r") as f:
            flipper_data = json.load(f)

        # Convert Flipper JSON to HAR format
        har_data = convert_flipper_to_har(flipper_data)

        # Write HAR data to output file
        with open(output_file, "w") as f:
            json.dump(har_data, f, indent=4)

        print(f"✅ Conversion successful. HAR data saved to {output_file}")

    except FileNotFoundError:
        print(f"❌ Input file '{input_file}' not found.")
    except json.JSONDecodeError:
        print(f"❌ Error parsing JSON from input file '{input_file}'.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
