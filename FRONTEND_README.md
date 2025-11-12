# K1 Watermark Frontend

A modern web-based frontend for configuring and executing K1 watermark processing scripts.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

**Windows:**
```bash
start_frontend.bat
```

**Manual Start:**
```bash
py server.py
```

### 3. Open in Browser

Navigate to: **http://localhost:5000**

## 📋 Features

### Configuration Options
- **FINAL_V2**: Text watermark configuration with custom text "hamacak1.com"
- **FINAL_V3**: PNG watermark configuration with `k1_watermark.png`
- **Glow Effect**: Professional glow effect with zero offset and high blur
- **Dramatic Shadow**: Large shadow offset with high blur
- **Custom**: Create your own custom configuration

### Input/Output Configuration
- Configure base input folder (parent folder containing subfolders)
- Configure base output folder (where processed images will be saved)
- Validate paths before processing
- View subfolder count in input directory

### Advanced Settings
- Custom text watermark
- Google Font selection
- PNG X/Y offset positioning
- Number X/Y offset positioning
- Parallel processing workers
- Dry run mode (preview without processing)
- Verbose logging

### Quick Commands Reference
The frontend displays all quick commands from `K1_QUICK_REFERENCE.md` (lines 1-40):
- FINAL_V2 Configuration command
- FINAL_V3 Configuration command
- Custom PNG Watermark with Offset command

## 🎯 Usage

1. **Select Configuration**: Choose from available configurations (final_v2, final_v3, etc.)
2. **Set Folders**: Enter base input and output folder paths
3. **Optional Settings**: Configure parallel workers, dry run, or verbose logging
4. **Advanced Settings**: Click "Advanced Settings" to configure custom options
5. **Validate**: Click "Validate Paths" to check folder structure
6. **Execute**: Click "Execute Processing" to start watermark processing

## 🔧 API Endpoints

### GET `/api/configs`
Returns available configurations.

### POST `/api/execute`
Executes the watermark processing command.

**Request Body:**
```json
{
  "base_input": "k1_test_input",
  "base_output": "k1_output",
  "config": "final_v3",
  "parallel": 1,
  "dry_run": false,
  "verbose": false,
  "custom_settings": {
    "png_x_offset": "50",
    "png_y_offset": "-20"
  }
}
```

### POST `/api/validate`
Validates input and output paths.

**Request Body:**
```json
{
  "base_input": "k1_test_input",
  "base_output": "k1_output"
}
```

## 📁 File Structure

```
watermark-01/
├── frontend.html          # Frontend UI (HTML/CSS/JavaScript)
├── server.py              # Flask backend server
├── start_frontend.bat     # Windows startup script
├── k1_multi_folder.py     # Main watermark processing script
└── requirements.txt       # Python dependencies (includes Flask)
```

## 🎨 Frontend Features

- **Modern UI**: Beautiful gradient design with responsive layout
- **Real-time Validation**: Check paths before processing
- **Live Output**: See command execution results in real-time
- **Quick Reference**: Built-in quick commands display
- **Error Handling**: Clear error messages and status indicators
- **Loading States**: Visual feedback during processing

## 🔍 Troubleshooting

### Server Won't Start
- Ensure Flask is installed: `pip install Flask flask-cors`
- Check if port 5000 is available
- Verify Python is in your PATH

### Path Validation Fails
- Ensure input folder exists and contains subfolders
- Check folder permissions
- Use absolute paths if relative paths don't work

### Command Execution Fails
- Check the output panel for detailed error messages
- Verify `k1_multi_folder.py` is in the same directory
- Ensure input folder contains valid image subfolders

## 📝 Notes

- The frontend runs on `http://localhost:5000` by default
- The server must be running for the frontend to work
- All commands are executed relative to the server's working directory
- Output is displayed in real-time in the output panel

## 🆘 Support

For issues or questions:
1. Check the output panel for error details
2. Review `k1_multi_folder.log` for processing logs
3. Verify all paths and configurations are correct
4. Use "Dry Run" mode to preview without processing

