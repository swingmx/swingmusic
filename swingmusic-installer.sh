#!/bin/bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "This script should not be run as root"
        exit 1
    fi
}

# Detect OS and architecture
detect_platform() {
    local os
    local arch
    
    case "$(uname -s)" in
        Linux*)     os="linux" ;;
        Darwin*)    os="macos" ;;
        *)          log_error "Unsupported operating system: $(uname -s)"; exit 1 ;;
    esac
    
    case "$(uname -m)" in
        x86_64)    arch="x86_64" ;;
        aarch64)   arch="aarch64" ;;
        arm64)     arch="aarch64" ;;
        *)         log_error "Unsupported architecture: $(uname -m)"; exit 1 ;;
    esac
    
    echo "${os}_${arch}"
}

# Check required commands
check_requirements() {
    local missing_commands=()
    
    for cmd in curl wget tar; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_commands+=("$cmd")
        fi
    done
    
    if [[ ${#missing_commands[@]} -gt 0 ]]; then
        log_error "Missing required commands: ${missing_commands[*]}"
        log_info "Please install the missing commands and try again"
        exit 1
    fi
}

# Install system dependencies (libev)
install_system_deps() {
    log_info "Installing system dependencies..."
    
    case "$(uname -s)" in
        Linux*)
            if command -v apt-get &> /dev/null; then
                log_info "Installing libev-dev via apt-get..."
                sudo apt-get update -qq
                sudo apt-get install -y ffmpeg libev-dev libavcodec-extra
            elif command -v dnf &> /dev/null; then
                log_info "Installing libev-devel via dnf..."
                sudo dnf install -y libev-devel
            elif command -v pacman &> /dev/null; then
                log_info "Installing libev via pacman..."
                sudo pacman -S --noconfirm libev
            elif command -v yum &> /dev/null; then
                log_info "Installing libev-devel via yum..."
                sudo yum install -y libev-devel
            else
                log_warning "Could not detect package manager for libev installation"
                log_info "Please install libev manually and try again"
                log_info "See README.md for installation instructions"
            fi
            ;;
        Darwin*)
            if command -v brew &> /dev/null; then
                log_info "Installing libev via Homebrew..."
                export HOMEBREW_NO_AUTO_UPDATE=1
                brew install libev
            else
                log_warning "Homebrew not found. Please install libev manually:"
                log_info "brew install libev"
                exit 1
            fi
            ;;
        *)
            log_error "Unsupported operating system for automatic libev installation"
            log_info "Please install libev manually and try again"
            exit 1
            ;;
    esac
    
    log_success "System dependencies installed successfully"
}

# Download file with fallback
download_file() {
    local url="$1"
    local output="$2"
    
    if command -v curl &> /dev/null; then
        curl -L -o "$output" "$url" --progress-bar
    elif command -v wget &> /dev/null; then
        wget -O "$output" "$url" --progress=bar
    else
        log_error "Neither curl nor wget is available"
        exit 1
    fi
}

# Install uv
install_uv() {
    # Check if uv is already installed
    if command -v uv &> /dev/null; then
        log_info "uv is already installed, checking version..."
        local uv_version
        uv_version=$(uv --version 2>/dev/null || echo "unknown")
        log_success "$uv_version is already available"
        return 0
    fi
    
    log_info "Installing uv..."
    
    local temp_dir
    temp_dir=$(mktemp -d)
    cd "$temp_dir"
    
    # Download uv installer
    log_info "Downloading uv installer..."
    download_file "https://astral.sh/uv/install.sh" "install.sh"
    
    # Make executable and run
    chmod +x install.sh
    UV_NO_MODIFY_PATH=1 ./install.sh
    
    cd - > /dev/null
    rm -rf "$temp_dir"
    
    # Verify installation
    if ! command -v uv &> /dev/null; then
        log_error "uv installation failed"
        exit 1
    fi
    
    log_success "uv installed successfully"
}

# Determine installation directory
get_install_dir() {
    if [[ -n "${XDG_BIN_HOME:-}" ]]; then
        echo "$XDG_BIN_HOME"
    elif [[ -n "${XDG_DATA_HOME:-}" ]]; then
        echo "$XDG_DATA_HOME/../bin"
    else
        echo "$HOME/.local/bin"
    fi
}

# Download and extract SwingMusic
install_swingmusic() {
    local install_dir
    install_dir=$(get_install_dir)
    
    # Create SwingMusic directory
    local swingmusic_dir="$install_dir/swingmusic-src"
    
    log_info "Installing SwingMusic source to $swingmusic_dir"
    
    # Create installation directory
    mkdir -p "$install_dir"
    
    if [[ -d "$swingmusic_dir" ]]; then
        log_warning "SwingMusic directory already exists, removing..."
        rm -rf "$swingmusic_dir"
    fi
    
    # Download latest source
    log_info "Downloading SwingMusic source..."
    local temp_dir
    temp_dir=$(mktemp -d)
    cd "$temp_dir"
    
    # Get latest release info and download source
    local latest_version
    latest_version=$(curl -s "https://api.github.com/repos/swingmx/swingmusic/releases/latest" | grep '"tag_name"' | cut -d'"' -f4)
    
    if [[ -z "$latest_version" ]]; then
        log_error "Failed to get latest version from GitHub"
        exit 1
    fi
    
    log_info "Latest version: $latest_version"
    
    local source_url="https://github.com/swingmx/swingmusic/archive/refs/tags/${latest_version}.tar.gz"
    log_info "Downloading from: $source_url"
    download_file "$source_url" "swingmusic.tar.gz"
    
    # Extract
    log_info "Extracting source..."
    tar -xzf swingmusic.tar.gz > /dev/null 2>&1
    
    # Move to installation directory
    local extracted_dir
    extracted_dir=$(ls -d swingmusic-*)
    mv "$extracted_dir" "$swingmusic_dir"
    
    cd - > /dev/null
    rm -rf "$temp_dir"
    
    log_success "SwingMusic source extracted to $swingmusic_dir"
    # Install dependencies
    log_info "Installing dependencies..."
    cd "$swingmusic_dir"
    # log current directory
    log_info "Current directory: $(pwd)"
    
    # Check Python version and create virtual environment if needed
    log_info "Checking Python version..."
    local python_version
    
    # First try to check system Python directly
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version 2>/dev/null | cut -d' ' -f2)
    elif command -v python &> /dev/null; then
        python_version=$(python --version 2>/dev/null | cut -d' ' -f2)
    fi
    
    # If no suitable Python found, create venv with specific version
    if [[ -z "$python_version" ]] || [[ ! "$python_version" =~ ^3\.(1[1-9]|[2-9][0-9]) ]]; then
        log_info "Python 3.11+ not found, creating virtual environment with Python 3.11..."
        UV_VENV_CLEAR=1 uv venv --python 3.11
    else
        log_info "Found Python $python_version, using existing environment"
    fi
    
    
    # Install dependencies
    uv sync
    
    log_success "Dependencies installed successfully"
}

# Create swingmusic command
create_command() {
    local install_dir
    install_dir=$(get_install_dir)
    
    local command_path="$install_dir/swingmusic"
    local swingmusic_dir="$install_dir/swingmusic-src"
    
    log_info "Creating swingmusic command..."
    
    # Create the command script
    cat > "$command_path" << 'EOF'
#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SWINGMUSIC_DIR="$SCRIPT_DIR/swingmusic-src"

# Check if SwingMusic directory exists
if [[ ! -d "$SWINGMUSIC_DIR" ]]; then
    echo "Error: SwingMusic installation not found at $SWINGMUSIC_DIR"
    exit 1
fi

# Change to SwingMusic directory and run
cd "$SWINGMUSIC_DIR"
uv run python -m swingmusic "$@"
EOF
    
    # Make executable
    chmod +x "$command_path"
    
    log_success "swingmusic command created at $command_path"
    
    # Check if the directory is in PATH
    if [[ ":$PATH:" != *":$install_dir:"* ]]; then
        log_warning "The installation directory $install_dir is not in your PATH"
        log_info "To use the swingmusic command, add this line to your shell profile:"
        echo "export PATH=\"$install_dir:\$PATH\""
        
        # Try to detect shell and suggest the right file
        local shell_profile
        case "$SHELL" in
            */zsh)  shell_profile="$HOME/.zshrc" ;;
            */bash) shell_profile="$HOME/.bashrc" ;;
            *)      shell_profile="$HOME/.profile" ;;
        esac
        
        if [[ -f "$shell_profile" ]]; then
            log_info "Or add it to: $shell_profile"
        fi
    else
        log_success "Installation directory is already in PATH"
    fi
}

# Main installation function
main() {
    log_info "Starting SwingMusic installation..."
    
    # Check if not running as root
    check_root
    
    # Check requirements
    check_requirements
    
    # Detect platform
    local platform
    platform=$(detect_platform)
    log_info "Detected platform: $platform"
    
    # Install system dependencies
    install_system_deps
    
    # Install uv
    install_uv
    
    # Install SwingMusic
    install_swingmusic
    
    # Create command
    create_command
    
    log_success "SwingMusic installation completed successfully!"
    log_info "You can now run: swingmusic --help"
}

# Run main function
main "$@"
