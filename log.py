import os
import subprocess
import zipfile
import shutil
import platform

# Function to execute commands via adb
def adb_command(command):
    process = subprocess.Popen(['adb'] + command, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode('utf-8', errors='replace').strip()

# Function to collect logs
def collect_logs():
    # Create a temporary directory to store logs
    temp_dir = 'temp_logs'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Collect logs
    log_commands = [
        ['logcat', '-d'],  # System logs
        ['bugreport'],  # Bug report
        ['dumpsys', 'battery'],  # Battery information
        ['dumpsys', 'wifi'],  # Wi-Fi information
        ['dumpsys', 'audio'],  # Audio information
        ['dumpsys', 'cpuinfo'],  # CPU information
        ['dumpsys', 'meminfo'],  # Memory information
        ['dumpsys', 'telephony'],  # Telephony information
        ['dumpsys', 'activity'],  # Current activity information
        ['dumpsys', 'location'],  # Location information
        ['dumpsys', 'package'],  # Application package information
        ['dumpsys', 'netstats'],  # Network statistics
        ['dumpsys', 'media.audio_flinger'],  # Audio flinger information
        ['dumpsys', 'sensorservice'],  # Sensor service information
        ['dumpsys', 'usagestats'],  # Application usage statistics
        ['dumpsys', 'batteryinfo'],  # Battery information (additional)
        ['dumpsys', 'wifi', 'supplicant'],  # Wi-Fi supplicant information
        # Add other commands for log collection if needed
    ]

    for cmd in log_commands:
        output = adb_command(cmd)
        with open(os.path.join(temp_dir, '_'.join(cmd) + '.log'), 'w', encoding='utf-8') as f:
            f.write(output)

    # Create a zip archive
    zip_filename = 'device_logs.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

    # Remove the temporary directory based on the operating system
    if platform.system() == 'Windows':
        os.system('rmdir /s /q {}'.format(temp_dir))  # Delete directory on Windows
    else:
        shutil.rmtree(temp_dir)  # Delete directory on Linux

    print("Logs successfully collected and saved in", zip_filename)

# Call the function to collect logs
collect_logs()
