import subprocess
import shlex
import os

# Define allowed commands
ALLOWED_COMMANDS = {
    "ls": [],
    "grep": ["-R"],
}

def run_whitelisted_command(command_name: str, user_args_string: str = ""):
    """
    Executes a predefined, whitelisted system command with user-provided arguments.
    This prevents arbitrary command execution and protects against shell injection.
    """
    if command_name not in ALLOWED_COMMANDS:
        raise ValueError(f"Command '{command_name}' is not permitted.")

    command_list = [command_name]
    command_list.extend(ALLOWED_COMMANDS[command_name])

    if user_args_string:
        parsed_user_args = shlex.split(user_args_string)
        command_list.extend(parsed_user_args)

    try:
        result = subprocess.run(
            command_list,
            shell=False,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Command executed successfully: {' '.join(command_list)}")
        print("Output:", result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        raise
    except FileNotFoundError:
        print(f"Error: Command '{command_name}' not found.")
        raise

# Get API key from environment (secure way)
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")