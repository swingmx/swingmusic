#!/bin/bash
# shellcheck shell=dash
# shellcheck disable=SC2039  # local is non-POSIX
#
# Licensed under the AGPLv3 license
# <LICENSE-AGPLv3 or https://www.gnu.org/licenses/agpl-3.0.html>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

# This runs on Unix shells like bash/dash/ksh/zsh. It uses the common `local`
# extension. Note: Most shells limit `local` to 1 var per line, contra bash.

# Some versions of ksh have no `local` keyword. Alias it to `typeset`, but
# beware this makes variables global with f()-style function syntax in ksh93.
# mksh has this alias by default.
has_local() {
    # shellcheck disable=SC2034  # deliberately unused
    local _has_local
}

has_local 2>/dev/null || alias local=typeset

set -euo pipefail

# Global variables
VERBOSE=${VERBOSE:-0}
QUIET=${QUIET:-0}

# No global verbose options - handled by say_verbose() function

# Utility functions
say() {
    if [ "$QUIET" = "0" ]; then
        printf '%s\n' "$1" >&2
    fi
}

say_verbose() {
    if [ "$VERBOSE" = "1" ]; then
        printf '\033[90m%s\033[0m\n' "$1" >&2
    fi
}

err() {
    printf '%s\n' "$1" >&2
    exit 1
}

warn() {
    printf '%s\n' "$1" >&2
}

need_cmd() {
    if ! command -v "$1" >/dev/null 2>&1; then
        err "need '$1' (command not found)"
    fi
}

ensure() {
    if ! "$@"; then
        err "command failed: $*"
    fi
}

get_home() {
    if [ -n "${HOME:-}" ]; then
        echo "$HOME"
    elif [ -n "${USER:-}" ]; then
        getent passwd "$USER" | cut -d: -f6
    else
        getent passwd "$(id -un)" | cut -d: -f6
    fi
}

# System detection functions
get_architecture() {
    local os_type
    local arch
    
    os_type=$(uname -s)
    arch=$(uname -m)
    
    case "$os_type" in
        "Darwin")
            case "$arch" in
                "x86_64")
                    echo "x86_64-apple-darwin"
                    ;;
                "arm64")
                    echo "aarch64-apple-darwin"
                    ;;
                *)
                    echo "unknown-apple-darwin"
                    ;;
            esac
            ;;
        "Linux")
            case "$arch" in
                "x86_64")
                    echo "x86_64-unknown-linux-gnu"
                    ;;
                "aarch64"|"arm64")
                    echo "aarch64-unknown-linux-gnu"
                    ;;
                "armv7l")
                    echo "armv7-unknown-linux-gnueabihf"
                    ;;
                *)
                    echo "unknown-unknown-linux-gnu"
                    ;;
            esac
            ;;
        *)
            echo "unknown-unknown-unknown"
            ;;
    esac
}

get_os_type() {
    local os_type
    local distro
    
    os_type=$(uname -s)
    
    case "$os_type" in
        "Darwin")
            echo "macos"
            ;;
        "Linux")
            if [ -f /etc/os-release ]; then
                distro=$(grep '^ID=' /etc/os-release | cut -d'=' -f2 | tr -d '"')
                case "$distro" in
                    "ubuntu"|"debian"|"pop"|"linuxmint"|"elementary")
                        echo "debian"
                        ;;
                    "arch"|"manjaro"|"endeavouros"|"garuda")
                        echo "arch"
                        ;;
                    "fedora"|"centos"|"rhel"|"rocky"|"alma")
                        echo "redhat"
                        ;;
                    "alpine")
                        echo "alpine"
                        ;;
                    *)
                        echo "linux"
                        ;;
                esac
            else
                echo "linux"
            fi
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

get_package_manager() {
    local os_type
    
    os_type=$(get_os_type)
    
    case "$os_type" in
        "debian")
            if command -v apt >/dev/null 2>&1; then
                echo "apt"
            else
                echo "unknown"
            fi
            ;;
        "arch")
            if command -v pacman >/dev/null 2>&1; then
                echo "pacman"
            else
                echo "unknown"
            fi
            ;;
        "redhat")
            if command -v dnf >/dev/null 2>&1; then
                echo "dnf"
            elif command -v yum >/dev/null 2>&1; then
                echo "yum"
            else
                echo "unknown"
            fi
            ;;
        "alpine")
            if command -v apk >/dev/null 2>&1; then
                echo "apk"
            else
                echo "unknown"
            fi
            ;;
        "macos")
            if command -v brew >/dev/null 2>&1; then
                echo "brew"
            else
                echo "unknown"
            fi
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

check_python_version() {
    local cmd
    local version
    local major
    local minor

    # Try every candidate interpreter in order and accept the first one whose
    # version lands in the supported range (3.11-3.14). This keeps the scan
    # going past a rejected candidate so e.g. a 3.9 at /usr/bin/python3 does
    # not prevent us from finding a 3.12 at /usr/bin/python or elsewhere.
    for cmd in python3.11 python3.12 python3.13 python3.14 python3 python; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            continue
        fi

        version=$("$cmd" --version 2>/dev/null | cut -d' ' -f2)
        if [ -z "$version" ]; then
            say_verbose "  $cmd: could not determine version"
            continue
        fi

        major=$(echo "$version" | cut -d'.' -f1)
        minor=$(echo "$version" | cut -d'.' -f2)

        if [ "$major" -eq 3 ] && [ "$minor" -ge 11 ] && [ "$minor" -le 14 ]; then
            say_verbose "  $cmd: $version (accepted)"
            echo "$cmd"
            return 0
        fi

        say_verbose "  $cmd: $version (rejected, need 3.11-3.14)"
    done

    return 1
}

# Main installation functions will be added in next phase

# Phase 2: Platform-Specific Logic
install_debian_dependencies() {
    local pkg_manager="$1"
    local python_version="$2"
    
    say "Installing dependencies for Debian-based system..."
    say_verbose "Using package manager: $pkg_manager"
    
    # Update package list
    say_verbose "Updating package list..."
    ensure sudo "$pkg_manager" update
    
    # Check if Python 3.11+ packages are available
    local python_pkg=""
    if [ "$python_version" = "3.11" ]; then
        if "$pkg_manager" list python3.11 2>/dev/null | grep -q python3.11; then
            python_pkg="python3.11"
        fi
    elif [ "$python_version" = "3.12" ]; then
        if "$pkg_manager" list python3.12 2>/dev/null | grep -q python3.12; then
            python_pkg="python3.12"
        fi
    fi
    
    # If specific Python version not available, try to add deadsnakes PPA (Ubuntu)
    if [ -z "$python_pkg" ] && command -v add-apt-repository >/dev/null 2>&1; then
        say_verbose "Adding deadsnakes PPA for Python $python_version..."
        ensure sudo add-apt-repository ppa:deadsnakes/ppa -y
        ensure sudo "$pkg_manager" update
        python_pkg="python$python_version"
    fi
    
    # Install Python if needed
    if [ -n "$python_pkg" ]; then
        say_verbose "Installing $python_pkg..."
        ensure sudo "$pkg_manager" install -y "$python_pkg" "${python_pkg}-venv" "${python_pkg}-dev"
    fi
    
    # Install system dependencies
    say_verbose "Installing system dependencies..."
    ensure sudo "$pkg_manager" install -y ffmpeg libev-dev build-essential
    
    # Install curl if not present
    if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
        say_verbose "Installing curl..."
        ensure sudo "$pkg_manager" install -y curl
    fi
    
    say "Debian dependencies installed successfully"
}

install_arch_dependencies() {
    local pkg_manager="$1"
    local python_version="$2"
    
    say "Installing dependencies for Arch-based system..."
    say_verbose "Using package manager: $pkg_manager"
    
    # Update package database
    say_verbose "Updating package database..."
    ensure sudo "$pkg_manager" -Sy
    
    # Install Python
    say_verbose "Installing Python $python_version..."
    ensure sudo "$pkg_manager" -S --noconfirm python python-pip
    
    # Install system dependencies
    say_verbose "Installing system dependencies..."
    ensure sudo "$pkg_manager" -S --noconfirm ffmpeg libev base-devel
    
    # Install curl if not present
    if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
        say_verbose "Installing curl..."
        ensure sudo "$pkg_manager" -S --noconfirm curl
    fi
    
    say "Arch dependencies installed successfully"
}

install_redhat_dependencies() {
    local pkg_manager="$1"
    local python_version="$2"
    
    say "Installing dependencies for Red Hat-based system..."
    say_verbose "Using package manager: $pkg_manager"
    
    # Update package database
    say_verbose "Updating package database..."
    ensure sudo "$pkg_manager" update -y
    
    # Enable EPEL repository if needed
    if [ "$pkg_manager" = "dnf" ] && ! "$pkg_manager" list epel-release >/dev/null 2>&1; then
        say_verbose "Enabling EPEL repository..."
        ensure sudo "$pkg_manager" install -y epel-release
    fi
    
    # Install Python
    say_verbose "Installing Python $python_version..."
    if [ "$python_version" = "3.11" ]; then
        ensure sudo "$pkg_manager" install -y python3.11 python3.11-devel
    elif [ "$python_version" = "3.12" ]; then
        ensure sudo "$pkg_manager" install -y python3.12 python3.12-devel
    fi
    
    # Install system dependencies
    say_verbose "Installing system dependencies..."
    ensure sudo "$pkg_manager" install -y ffmpeg libev-devel gcc make
    
    # Install curl if not present
    if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
        say_verbose "Installing curl..."
        ensure sudo "$pkg_manager" install -y curl
    fi
    
    say "Red Hat dependencies installed successfully"
}

install_alpine_dependencies() {
    local pkg_manager="$1"
    local python_version="$2"
    
    say "Installing dependencies for Alpine Linux..."
    say_verbose "Using package manager: $pkg_manager"
    
    # Update package database
    say_verbose "Updating package database..."
    ensure sudo "$pkg_manager" update
    
    # Install Python
    say_verbose "Installing Python $python_version..."
    ensure sudo "$pkg_manager" add python3 py3-pip
    
    # Install system dependencies
    say_verbose "Installing system dependencies..."
    ensure sudo "$pkg_manager" add ffmpeg libev-dev build-base
    
    # Install curl if not present
    if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
        say_verbose "Installing curl..."
        ensure sudo "$pkg_manager" add curl
    fi
    
    say "Alpine dependencies installed successfully"
}

install_macos_dependencies() {
    local pkg_manager="$1"
    local python_version="$2"
    
    say "Installing dependencies for macOS..."
    say_verbose "Using package manager: $pkg_manager"
    
    # Check if Homebrew is installed
    if ! command -v brew >/dev/null 2>&1; then
        say "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH for current session
        if [ -f /opt/homebrew/bin/brew ]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        elif [ -f /usr/local/bin/brew ]; then
            eval "$(/usr/local/bin/brew shellenv)"
        fi
    fi
    
    # Install Python
    say_verbose "Installing Python $python_version..."
    if [ "$python_version" = "3.11" ]; then
        ensure brew install python@3.11
    elif [ "$python_version" = "3.12" ]; then
        ensure brew install python@3.12
    fi
    
    # Install system dependencies
    say_verbose "Installing system dependencies..."
    ensure brew install ffmpeg libev
    
    # Install curl if not present
    if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
        say_verbose "Installing curl..."
        ensure brew install curl
    fi
    
    say "macOS dependencies installed successfully"
}

# Platform-specific dependency installer
install_platform_dependencies() {
    local os_type
    local pkg_manager
    local python_version
    
    os_type=$(get_os_type)
    pkg_manager=$(get_package_manager)
    python_version="3.11"  # Default to 3.11
    
    say_verbose "Detected OS: $os_type"
    say_verbose "Detected package manager: $pkg_manager"
    
    if [ "$pkg_manager" = "unknown" ]; then
        err "Unsupported package manager for OS: $os_type"
    fi
    
    case "$os_type" in
        "debian")
            install_debian_dependencies "$pkg_manager" "$python_version"
            ;;
        "arch")
            install_arch_dependencies "$pkg_manager" "$python_version"
            ;;
        "redhat")
            install_redhat_dependencies "$pkg_manager" "$python_version"
            ;;
        "alpine")
            install_alpine_dependencies "$pkg_manager" "$python_version"
            ;;
        "macos")
            install_macos_dependencies "$pkg_manager" "$python_version"
            ;;
        *)
            err "Unsupported OS type: $os_type"
            ;;
    esac
}

# Phase 3: Python Environment Management
install_python() {
    local python_cmd

    say "Checking Python installation..."

    # Check if suitable Python already exists (allow failure)
    python_cmd=$(check_python_version || true)
    if [ -n "$python_cmd" ]; then
        say "Found suitable Python: $python_cmd"
        say_verbose "Python version: $($python_cmd --version 2>/dev/null)"
        return 0
    fi

    say "No suitable Python found, installing dependencies..."
    install_platform_dependencies

    # Check again after installing dependencies (allow failure)
    python_cmd=$(check_python_version || true)
    if [ -n "$python_cmd" ]; then
        say "Python installed successfully: $python_cmd"
        return 0
    fi

    err "Failed to install suitable Python version"
}

# Determine installation directory using path resolution
get_install_dir() {
    if [ -n "${XDG_BIN_HOME:-}" ]; then
        echo "$XDG_BIN_HOME"
    elif [ -n "${XDG_DATA_HOME:-}" ]; then
        echo "$XDG_DATA_HOME/../bin"
    else
        echo "$(get_home)/.local/bin"
    fi
}

create_virtual_environment() {
    local install_dir
    local venv_dir
    local python_cmd
    
    install_dir=$(get_install_dir)
    venv_dir="$install_dir/swingmusic-venv"
    python_cmd=$(check_python_version || true)

    if [ -z "$python_cmd" ]; then
        err "No suitable Python found for virtual environment"
    fi
    
    say "Creating virtual environment in $venv_dir..."
    say_verbose "Using Python: $python_cmd"
    
    # Create base directory structure
    ensure mkdir -p "$install_dir"
    
    # Remove existing venv if it exists
    if [ -d "$venv_dir" ]; then
        say_verbose "Removing existing virtual environment..."
        rm -rf "$venv_dir"
    fi
    
    # Create virtual environment
    say_verbose "Creating virtual environment with $python_cmd..."
    ensure "$python_cmd" -m venv "$venv_dir"
    
    # Verify venv creation
    if [ ! -f "$venv_dir/bin/activate" ]; then
        err "Failed to create virtual environment"
    fi
    
    say "Virtual environment created successfully"
    printf '%s' "$venv_dir"
}

# Create wrapper script to make swingmusic command accessible
create_wrapper_script() {
    local install_dir
    local venv_dir
    local wrapper_script
    
    install_dir=$(get_install_dir)
    venv_dir="$1"
    wrapper_script="$install_dir/swingmusic"
    
    say "Creating wrapper script in $install_dir..."
    
    # Create wrapper script
    cat > "$wrapper_script" << 'EOF'
#!/bin/sh
# Swing Music wrapper script
# This script activates the virtual environment and runs swingmusic

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/swingmusic-venv"

# Check if virtual environment exists
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR" >&2
    exit 1
fi

# Activate virtual environment
. "$VENV_DIR/bin/activate"

# Handle --upgrade flag
if [ "$1" = "--upgrade" ]; then
    echo "Swing Music Upgrade"
    echo "==================="
    echo ""

    # Show current version
    CURRENT_VERSION=$(python -P -m swingmusic --version 2>/dev/null | head -n1)
    echo "Current version: $CURRENT_VERSION"
    echo ""

    # Preview the version pip will resolve before committing to the upgrade.
    # --only-binary swingmusic forces a wheel match: if no compatible wheel
    # exists for this interpreter/platform, pip fails here instead of silently
    # downgrading to an older version that happens to have an sdist.
    # `pip index versions` hits only the PyPI JSON API — no wheel downloads.
    echo "Resolving available version..."
    RESOLVED=$(pip index versions swingmusic --disable-pip-version-check 2>/dev/null \
        | head -n1 \
        | sed -nE 's/^swingmusic \(([^)]+)\).*/swingmusic-\1/p' || true)
    if [ -n "$RESOLVED" ]; then
        echo "Will upgrade to: $RESOLVED"
    fi
    echo ""

    # Perform upgrade
    echo "Upgrading Swing Music and dependencies..."
    if ! pip install --upgrade swingmusic --only-binary swingmusic --disable-pip-version-check; then
        echo "Error: Upgrade failed" >&2
        exit 1
    fi
    echo ""

    # Show new version
    NEW_VERSION=$(python -P -m swingmusic --version 2>/dev/null | head -n1)
    echo "Successfully upgraded to: $NEW_VERSION"
    echo ""

    # Detect OS and restart service
    OS_TYPE=$(uname -s)
    echo "Restarting Swing Music service..."

    case "$OS_TYPE" in
        "Darwin")
            # macOS - use launchctl
            if launchctl kickstart -k "gui/$(id -u)/com.swingmusic" 2>/dev/null; then
                echo "Service restarted successfully (macOS)"
            elif launchctl stop com.swingmusic 2>/dev/null && launchctl start com.swingmusic 2>/dev/null; then
                echo "Service restarted successfully (macOS)"
            else
                echo "Warning: Could not restart service automatically" >&2
                echo "Please restart manually: launchctl restart com.swingmusic" >&2
            fi
            ;;
        "Linux")
            # Linux - use systemctl
            if systemctl --user restart swingmusic.service 2>/dev/null; then
                echo "Service restarted successfully (Linux)"
            else
                echo "Warning: Could not restart service automatically" >&2
                echo "Please restart manually: systemctl --user restart swingmusic" >&2
            fi
            ;;
        *)
            echo "Warning: Unknown OS type: $OS_TYPE" >&2
            echo "Please restart the service manually" >&2
            ;;
    esac

    echo ""
    echo "Upgrade complete!"
    exit 0
fi

# Run swingmusic with all arguments (normal operation).
exec python -P -m swingmusic "$@"
EOF
    
    # Make wrapper script executable
    ensure chmod +x "$wrapper_script"
    
    say "Wrapper script created successfully"
    printf '%s' "$wrapper_script"
}

install_swingmusic() {
    local venv_dir
    local python_cmd
    local pip_cmd
    
    venv_dir="$1"
    
    say_verbose "Installing Swing Music in virtual environment..."
    say_verbose "Virtual environment: $venv_dir"

    # Get Python and pip commands from virtual environment
    python_cmd="$venv_dir/bin/python"
    pip_cmd="$venv_dir/bin/pip"
    
    # Verify Python and pip exist in the virtual environment
    if [ ! -x "$python_cmd" ]; then
        err "Python not found in virtual environment: $python_cmd"
    fi
    
    if [ ! -x "$pip_cmd" ]; then
        err "pip not found in virtual environment: $pip_cmd"
    fi

    
    # Preview the version pip will resolve before committing to the install.
    # --only-binary swingmusic forces a wheel match: if no compatible wheel exists
    # for this interpreter/platform, pip fails here instead of silently
    # downgrading to an older version that happens to have an sdist.
    # `pip index versions` hits only the PyPI JSON API and filters by
    # interpreter compatibility — no wheel downloads, no resolver work.
    # First line is "swingmusic (X.Y.Z)" where X.Y.Z is the best candidate.
    say "Resolving Swing Music version..."
    local resolved
    resolved=$("$pip_cmd" index versions swingmusic --disable-pip-version-check 2>/dev/null \
        | head -n1 \
        | sed -nE 's/^swingmusic \(([^)]+)\).*/swingmusic-\1/p' || true)
    if [ -n "$resolved" ]; then
        say "Will install: $resolved"
    else
        say_verbose "Could not preview version"
    fi

    # Install Swing Music
    say "Installing Swing Music. This may take a while..."
    ensure "$pip_cmd" install swingmusic --only-binary swingmusic --disable-pip-version-check --quiet

    # Verify installation
    say "Verifying installation..."
    local verify_output
    if ! verify_output=$("$python_cmd" -P -m swingmusic --version 2>&1); then
        printf '%s\n' "$verify_output" >&2
        err "Failed to verify Swing Music installation"
    fi

    local version
    version=$(printf '%s' "$verify_output" | head -n1)
    say "Swing Music installed successfully: $version"
}

# Kill all Swing Music processes
kill_swingmusic_processes() {
    say "Stopping Swing Music processes..."
    say_verbose "Searching for running Swing Music processes"

    # Find and kill all Swing Music processes
    local killed_count=0

    # Use pkill to find and kill processes matching "swingmusic "
    if command -v pkill >/dev/null 2>&1; then
        say_verbose "Using pkill to find and kill processes"
        # Count processes before killing
        if command -v pgrep >/dev/null 2>&1; then
            killed_count=$(pgrep -f "swingmusic " 2>/dev/null | wc -l) || killed_count=0
            say_verbose "Found $killed_count Swing Music processes"
        fi

        # Kill all Swing Music processes
        if pkill -9 -f "swingmusic " >/dev/null 2>&1; then
            if [ "$killed_count" -gt 0 ]; then
                say "Killed $killed_count Swing Music process(es)"
                say_verbose "Successfully killed processes using SIGKILL"
            else
                say "No Swing Music processes found"
            fi
        else
            say "No Swing Music processes found"
        fi
    else
        say_verbose "pkill not available, using ps and kill fallback"
        # Fallback: use ps and kill manually
        local pids
        pids=$(ps aux | grep "swingmusic " | grep -v grep | awk '{print $2}')

        if [ -n "$pids" ]; then
            killed_count=$(echo "$pids" | wc -w)
            say_verbose "Found PIDs: $pids"
            for pid in $pids; do
                say_verbose "Killing process $pid"
                kill -9 "$pid" >/dev/null 2>&1
            done
            say "Killed $killed_count Swing Music process(es)"
        else
            say "No Swing Music processes found"
        fi
    fi
}

# Remove systemd service
remove_systemd_service() {
    local service_dir="$HOME/.config/systemd/user"
    local service_file="$service_dir/swingmusic.service"

    say "Removing systemd service..."
    say_verbose "Service directory: $service_dir"
    say_verbose "Service file: $service_file"

    # Check if systemd is available
    if ! command -v systemctl >/dev/null 2>&1; then
        say "systemd not available, skipping service removal"
        say_verbose "systemctl command not found"
        return 0
    fi

    # Stop the service
    say_verbose "Stopping systemd service: swingmusic.service"
    systemctl --user stop swingmusic.service >/dev/null 2>&1
    say "Stopped Swing Music service"

    # Disable the service
    say_verbose "Disabling systemd service: swingmusic.service"
    systemctl --user disable swingmusic.service >/dev/null 2>&1
    say "Disabled Swing Music service"

    # Remove service file
    if [ -f "$service_file" ]; then
        say_verbose "Removing service file: $service_file"
        if rm "$service_file" 2>/dev/null; then
            say "Removed: $service_file"
        else
            warn "Failed to remove: $service_file"
        fi
    else
        say "Service file not found: $service_file"
        say_verbose "Service file does not exist, nothing to remove"
    fi

    # Reload systemd
    say_verbose "Reloading systemd user daemon"
    systemctl --user daemon-reload >/dev/null 2>&1 || true
}

# Remove launchd service
remove_launchd_service() {
    local service_dir="$HOME/Library/LaunchAgents"
    local service_file="$service_dir/com.swingmusic.plist"

    say "Removing launchd service..."
    say_verbose "Service directory: $service_dir"
    say_verbose "Service file: $service_file"

    # Check if launchctl is available
    if ! command -v launchctl >/dev/null 2>&1; then
        say "launchctl not available, skipping service removal"
        say_verbose "launchctl command not found"
        return 0
    fi

    # Stop the service
    say_verbose "Stopping launchd service: com.swingmusic"
    launchctl stop com.swingmusic >/dev/null 2>&1 || true
    say "Stopped Swing Music service"

    # Unload the service
    say_verbose "Unloading launchd service: $service_file"
    launchctl unload "$service_file" >/dev/null 2>&1 || true
    say "Unloaded Swing Music service"

    # Remove service file
    if [ -f "$service_file" ]; then
        say_verbose "Removing service file: $service_file"
        if rm "$service_file" 2>/dev/null; then
            say "Removed: $service_file"
        else
            warn "Failed to remove: $service_file"
        fi
    else
        say "Service file not found: $service_file"
        say_verbose "Service file does not exist, nothing to remove"
    fi
}

# Remove wrapper script
remove_wrapper_script() {
    local install_dir
    local wrapper_script

    install_dir=$(get_install_dir)
    wrapper_script="$install_dir/swingmusic"

    say "Removing wrapper script..."
    say_verbose "Install directory: $install_dir"
    say_verbose "Wrapper script path: $wrapper_script"

    if [ -f "$wrapper_script" ]; then
        say_verbose "Removing wrapper script file"
        if rm "$wrapper_script" 2>/dev/null; then
            say "Removed: $wrapper_script"
        else
            warn "Failed to remove: $wrapper_script"
        fi
    else
        say "Wrapper script not found: $wrapper_script"
        say_verbose "Wrapper script does not exist, nothing to remove"
    fi
}

# Remove virtual environment
remove_virtual_environment() {
    local install_dir
    local venv_dir

    install_dir=$(get_install_dir)
    venv_dir="$install_dir/swingmusic-venv"

    say "Removing virtual environment..."
    say_verbose "Install directory: $install_dir"
    say_verbose "Virtual environment path: $venv_dir"

    if [ -d "$venv_dir" ]; then
        say_verbose "Removing virtual environment directory and contents"
        if rm -rf "$venv_dir" 2>/dev/null; then
            say "Removed: $venv_dir"
        else
            warn "Failed to remove: $venv_dir"
        fi
    else
        say "Virtual environment not found: $venv_dir"
        say_verbose "Virtual environment directory does not exist, nothing to remove"
    fi
}

# Main uninstall function
uninstall() {
    say "Starting Swing Music uninstallation..."
    say_verbose "Uninstall mode activated"
    say_verbose "OS type: $(get_os_type)"
    say ""

    # Stop and remove system services based on OS
    local os_type
    os_type=$(get_os_type)
    say_verbose "Detected OS type: $os_type"

    case "$os_type" in
        "macos")
            say_verbose "Running macOS service removal"
            remove_launchd_service
            ;;
        "linux"|"debian"|"arch"|"redhat"|"alpine")
            say_verbose "Running Linux systemd service removal"
            remove_systemd_service
            ;;
        *)
            say "Unknown OS, skipping service removal"
            say_verbose "Unsupported OS type: $os_type"
            ;;
    esac

    # Kill any remaining Swing Music processes
    kill_swingmusic_processes

    # Remove application files
    remove_wrapper_script
    remove_virtual_environment

    say ""
    say "Swing Music uninstalled successfully!"
    say_verbose "Uninstallation process completed"
}

# Test basic functionality
test_installation() {
    local wrapper_script
    local venv_dir
    
    wrapper_script="$1"
    venv_dir="$2"
    
    say "Testing installation..."
    
    # Test wrapper script
    if [ ! -x "$wrapper_script" ]; then
        err "Wrapper script is not executable"
    fi
    
    # Test swingmusic command
    if ! "$wrapper_script" --version >/dev/null 2>&1; then
        err "Swing Music command failed"
    fi
    
    local version
    version=$("$wrapper_script" --version 2>/dev/null | head -n1)
    say "Installation test successful: $version"
    
    # Test which command
    if ! command -v swingmusic >/dev/null 2>&1; then
        warn "swingmusic command not found in PATH (may need to restart shell)"
    else
        say "swingmusic command is available in PATH"
    fi
}

# Phase 4: System Integration
create_systemd_service() {
    local venv_dir
    local install_dir
    local service_dir
    local service_file
    
    venv_dir="$1"
    install_dir=$(get_install_dir)
    service_dir="$HOME/.config/systemd/user"
    service_file="$service_dir/swingmusic.service"
    
    say "Creating systemd service for Swing Music..."
    
    # Check if systemd is available
    if ! command -v systemctl >/dev/null 2>&1; then
        warn "systemd not available, skipping service creation"
        return 0
    fi
    
    # Create service directory
    ensure mkdir -p "$service_dir"
    
    # Create service file
    cat > "$service_file" << EOF
[Unit]
Description=Swing Music Server
After=network.target

[Service]
Type=simple
WorkingDirectory=$install_dir
Environment=PATH=$venv_dir/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=$venv_dir/bin/python -P -m swingmusic
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF
    
    # Reload systemd and enable service
    say_verbose "Reloading systemd user daemon..."
    ensure systemctl --user daemon-reload
    
    say_verbose "Enabling Swing Music service..."
    ensure systemctl --user enable swingmusic.service

    say_verbose "Starting Swing Music service..."
    ensure systemctl --user start swingmusic.service

    say "Systemd service created, enabled, and started successfully"
    say "Service file: $service_file"
    say ""
    say "Service Management Commands:"
    say "To start Swing Music service:"
    say "    systemctl --user start swingmusic"
    say ""
    say "To stop Swing Music service:"
    say "    systemctl --user stop swingmusic"
    say ""
    say "To check service status:"
    say "    systemctl --user status swingmusic"
    say ""
    say "To view service logs:"
    say "    journalctl --user -u swingmusic -f"
}

create_launchd_service() {
    local venv_dir
    local install_dir
    local service_dir
    local service_file
    
    venv_dir="$1"
    install_dir=$(get_install_dir)
    service_dir="$HOME/Library/LaunchAgents"
    service_file="$service_dir/com.swingmusic.plist"
    
    say "Creating launchd service for Swing Music..."
    
    # Create service directory
    ensure mkdir -p "$service_dir"
    
    # Create plist file
    cat > "$service_file" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.swingmusic</string>
    <key>Program</key>
    <string>$install_dir/swingmusic</string>
    <key>ProgramArguments</key>
    <array>
        <string>$install_dir/swingmusic</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$install_dir</string>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/swingmusic.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/swingmusic.error.log</string>
</dict>
</plist>
EOF
    
    # Load the service
    say_verbose "Loading Swing Music service..."
    ensure launchctl load "$service_file"
    
    say "Launchd service created and loaded successfully"
    say "Service file: $service_file"
    say ""
    say "Service Management Commands:"
    say "To start Swing Music service:"
    say "    launchctl start com.swingmusic"
    say ""
    say "To stop Swing Music service:"
    say "    launchctl stop com.swingmusic"
    say ""
    say "To check if service is running:"
    say "    launchctl list | grep swingmusic"
    say ""
    say "To view service logs:"
    say "    tail -f /tmp/swingmusic.log"
}

# Add swingmusic command to user's PATH
add_to_path() {
    local install_dir
    local shell_rc
    local path_line
    
    install_dir=$(get_install_dir)
    
    say "Adding Swing Music to PATH..."
    say_verbose "Installation directory: $install_dir"
    
    # Detect user's shell and appropriate rc file
    local shell_name
    shell_name=$(basename "$SHELL")
    
    case "$shell_name" in
        "bash")
            shell_rc="$HOME/.bashrc"
            ;;
        "zsh")
            shell_rc="$HOME/.zshrc"
            ;;
        "fish")
            shell_rc="$HOME/.config/fish/config.fish"
            ;;
        *)
            shell_rc="$HOME/.profile"
            ;;
    esac
    
    say_verbose "Using shell configuration file: $shell_rc"
    
    # Check if Swing Music path already exists in rc file
    if [ -f "$shell_rc" ] && grep -q "$install_dir" "$shell_rc"; then
        say "Swing Music PATH already configured in $shell_rc"
        return 0
    fi
    
    # Create rc file if it doesn't exist
    if [ ! -f "$shell_rc" ]; then
        ensure touch "$shell_rc"
    fi
    
    # Add path to rc file
    path_line="export PATH=\"$install_dir:\$PATH\""
    echo "" >> "$shell_rc"
    echo "# Swing Music installation" >> "$shell_rc"
    echo "$path_line" >> "$shell_rc"
    
    say "Added Swing Music to PATH in $shell_rc"
    say "Please restart your shell or run: source $shell_rc"
    
    # Also add to current session PATH
    export PATH="$install_dir:$PATH"
    say_verbose "Added to current session PATH"
}

# Main installation function
main() {
    local venv_dir
    local wrapper_script
    
    say "Starting Swing Music installation..."
    say_verbose "Architecture: $(get_architecture)"
    say_verbose "OS Type: $(get_os_type)"
    say_verbose "Package Manager: $(get_package_manager)"
    
    # Check for at least one download command
    if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
        err "Neither curl nor wget found. At least one is required for installation."
    fi
    
    # Install Python if needed
    install_python
    
    # Create virtual environment
    venv_dir=$(create_virtual_environment)
    
    # Install Swing Music
    install_swingmusic "$venv_dir"
    
    # Create wrapper script
    wrapper_script=$(create_wrapper_script "$venv_dir")
    
    # Test installation
    test_installation "$wrapper_script" "$venv_dir"
    
    # Add to PATH
    add_to_path
    
    # Create system service
    case "$(get_os_type)" in
        "macos")
            create_launchd_service "$venv_dir"
            ;;
        "linux"|"debian"|"arch"|"redhat"|"alpine")
            create_systemd_service "$venv_dir"
            ;;
        *)
            warn "Unsupported OS for service creation"
            ;;
    esac
    
    say ""
    say "Executable path: $wrapper_script"
    say "Installation directory: $venv_dir"
    say ""
    say "Installation completed successfully! 🎉"
    say "Open http://localhost:1970 in your browser to start using Swing Music"
    say ""
    say "To uninstall Swing Music, run:"
    say "    curl -fsSL https://setup.swingmx.com | bash -s -- --uninstall"
}

# Show usage information
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Install or uninstall Swing Music on Unix-based systems.

OPTIONS:
    -v, --verbose      Enable verbose output
    -q, --quiet        Suppress normal output
    -h, --help         Show this help message
    --uninstall        Uninstall Swing Music and remove all files

ENVIRONMENT VARIABLES:
    VERBOSE=1          Enable verbose output
    QUIET=1            Suppress normal output

EXAMPLES:
    $0                      # Normal installation
    $0 --verbose           # Verbose installation
    $0 --uninstall        # Uninstall Swing Music
    VERBOSE=1 $0          # Verbose installation via environment

EOF
}

# Parse command line arguments
UNINSTALL_MODE=0

while [ $# -gt 0 ]; do
    case "$1" in
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        -q|--quiet)
            QUIET=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --uninstall)
            UNINSTALL_MODE=1
            shift
            ;;
        *)
            err "Unknown option: $1"
            ;;
    esac
done

# Run appropriate function based on mode
if [ "$UNINSTALL_MODE" = "1" ]; then
    uninstall
else
    main
fi