# Simple Drawbot Software

A desktop application that converts drawings, text, and images into G-code for CNC machines, with a focus on pen plotters.

## Features

- 🎨 Drawing Interface with grid system and basic tools
- 📝 Text handling with size and rotation options
- 🖼️ Image processing capabilities
- ⚙️ Configurable machine settings
- 🔧 Standard G-code output format

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (included with Python)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Deejpotter/simple-drawbot-software.git
   cd simple-drawbot-software
   ```

2. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
4. Update dependencies file if needed:
   ```bash
   pip freeze > requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   # Make sure your virtual environment is activated
   python src/main.py
   ```

2. Configure your machine settings:
    - Set bed size
    - Configure tool parameters
    - Define safe zones

3. Create your design:
    - Use drawing tools
    - Import images
    - Add text

4. Generate and export G-code:
    - Preview the tool path
    - Adjust settings if needed
    - Save the G-code file

## Development

### Project Structure

```
gcode-generator/
├── src/
│   ├── gcode_generator/
│   │   ├── ui/         # User interface components
│   │   ├── core/       # Core functionality
│   │   └── utils/      # Utility functions
│   └── main.py
├── tests/              # Test files
├── docs/               # Documentation
└── examples/           # Example files
```

### Running Tests

```bash
# Make sure your virtual environment is activated
pytest
```

### Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

PySide6 is licensed under the LGPL-3.0 License.

