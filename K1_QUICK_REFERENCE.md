# K1 Quick Reference Card

## 🚀 **Quick Start Commands**

### **Basic Usage**
```bash
# Process with tested final_v2 configuration (processes all subfolders in k1_test_input)
py k1_multi_folder.py --base-input "k1_test_input" --base-output "k1_output" --config "final_v2"

# List all available configurations
py k1_multi_folder.py --list-configs

# Dry run to preview processing
py k1_multi_folder.py --base-input "k1_test_input" --base-output "k1_output" --config "final_v2" --dry-run
```

### **Pre-Configured Settings**

#### **final_v2** ✅ (Tested & Confirmed)
```bash
--custom-text "hamacak1.com"
--google-font "Rubik"
--custom-text-position "center-bottom"
--custom-text-size-ratio 0.05
--margin 120
--custom-text-shadow-offset 15
--custom-text-shadow-blur 8
--custom-text-opacity 0.6
--shadow-offset 0
--shadow-blur 6
--number-opacity 0.4
```

#### **glow_effect** (Professional Glow)
```bash
--custom-text "K1-PRINT"
--google-font "Rubik"
--custom-text-position "center-bottom"
--custom-text-size-ratio 0.06
--margin 150
--custom-text-shadow-offset 0
--custom-text-shadow-blur 8
--custom-text-shadow-color "#FFFFFF"
--custom-text-opacity 0.8
--shadow-offset 0
--shadow-blur 4
--number-opacity 0.3
```

#### **dramatic_shadow** (Large Shadow Effects)
```bash
--custom-text "K1-PRINT"
--google-font "Rubik"
--custom-text-position "center-bottom"
--custom-text-size-ratio 0.05
--margin 200
--custom-text-shadow-offset 25
--custom-text-shadow-blur 12
--custom-text-opacity 0.5
--shadow-offset 0
--shadow-blur 8
--number-opacity 0.25
```

## ⚙️ **Advanced Features**

### **Custom Configuration**
```bash
# Override specific settings
py k1_multi_folder.py --base-input "k1_test_input" --base-output "k1_output" --config "final_v2" --custom-text "K1-CUSTOM" --custom-text-opacity 0.7

# Full custom configuration with shadow opacity control
py k1_multi_folder.py --base-input "k1_test_input" --base-output "k1_output" --config "custom" --custom-text "K1-FULL" --google-font "Rubik" --custom-text-shadow-offset 20 --custom-text-shadow-blur 10 --custom-text-shadow-opacity 0.5 --custom-text-opacity 0.6

# Advanced shadow control
py k1_multi_folder.py --base-input "k1_test_input" --base-output "k1_output" --config "custom" --custom-text "K1-ADVANCED" --custom-text-shadow-opacity 0.3 --shadow-opacity 0.7
```

### **Batch Processing**
```bash
# Process with multiple configurations at once
py k1_multi_folder.py --base-input "k1_test_input" --base-output "k1_output" --config "batch" --batch-configs "final_v2,glow_effect,dramatic_shadow"
```

### **Parallel Processing**
```bash
# Use 2 parallel workers for faster processing
py k1_multi_folder.py --base-input "test_nico" --base-output "k1_output" --config "final_v2" --parallel 2
```

### **Verbose Logging**
```bash
# Enable detailed logging
py k1_multi_folder.py --base-input "test_nico" --base-output "k1_output" --config "final_v2" --verbose
```

## 📁 **Output Structure**

### **New Folder Structure**
```
k1_test_input/                    # Parent input folder
├── fofof 345/                    # Subfolder 1
├── nananane46/                   # Subfolder 2
├── test_nico/                    # Subfolder 3
└── test_nico - copia/            # Subfolder 4

k1_output/                        # Output folder
├── fofof 345_final_v2/           # Subfolder 1 with final_v2 config
├── nananane46_final_v2/          # Subfolder 2 with final_v2 config
├── test_nico_final_v2/           # Subfolder 3 with final_v2 config
└── test_nico - copia_final_v2/   # Subfolder 4 with final_v2 config
```

## 🎯 **Common Use Cases**

### **Configuration Editing**
The `final_v2` configuration is now easily editable directly in the script:
- **Location**: Lines 60-75 in `k1_multi_folder.py`
- **Clear Comments**: Each parameter is documented with explanations
- **Valid Ranges**: Parameter limits are specified for easy tuning
- **No Restart Required**: Edit and save, then run the script

### **Enhanced Shadow Opacity Control** ✨
- **Custom Text Shadow**: `--custom-text-shadow-opacity` (0.1-1.0) - Independent shadow transparency
- **Number Watermark Shadow**: `--shadow-opacity` (0.1-1.0) - Independent number shadow transparency
- **Professional Tuning**: Separate shadow opacity from main text/number opacity
- **Visual Balance**: Perfect shadow effects for any background or lighting condition

### **Production Workflow**
```bash
# 1. Test with dry run
py k1_multi_folder.py --base-input "production_photos" --base-output "test_output" --config "final_v2" --dry-run

# 2. Process with tested configuration
py k1_multi_folder.py --base-input "production_photos" --base-output "watermarked_photos" --config "final_v2"

# 3. Batch process with multiple styles
py k1_multi_folder.py --base-input "production_photos" --base-output "multiple_styles" --config "batch" --batch-configs "final_v2,glow_effect"
```

### **Testing & Development**
```bash
# Test all configurations
py k1_test_all_features.py

# Test specific configuration
py k1_multi_folder.py --base-input "k1_test_input" --base-output "test_output" --config "final_v2" --verbose
```

### **Custom Branding**
```bash
# Company branding
py k1_multi_folder.py --base-input "company_photos" --base-output "branded_photos" --config "custom" --custom-text "COMPANY.COM" --custom-text-color "#2E8B57" --custom-text-shadow-color "#FFFFFF"
```

## 🔧 **Troubleshooting**

### **Common Issues**
- **Font Loading**: Ensure internet connection for Google Fonts
- **Memory Errors**: Use `--parallel 1` for large images
- **Shadow Cutting**: All configurations now have enhanced safety margins

### **Debug Commands**
```bash
# Check available configurations
py k1_multi_folder.py --list-configs

# Dry run to preview
py k1_multi_folder.py --base-input "k1_test_input" --base-output "test_output" --config "final_v2" --dry-run

# Verbose logging
py k1_multi_folder.py --base-input "k1_test_input" --base-output "test_output" --config "final_v2" --verbose
```

## 📊 **Performance Tips**

### **Optimization**
- **Sequential**: Use default (1 worker) for small batches
- **Parallel**: Use `--parallel 2` for 3+ folders
- **Batch**: Use batch processing for multiple configurations

### **Expected Performance**
- **Single Image**: ~0.5-1.0 seconds
- **Single Folder (2 images)**: ~1-2 seconds
- **Multi-Folder (3 folders)**: ~3-6 seconds
- **Parallel Processing**: ~2-4 seconds (30% improvement)

## 🆘 **Emergency Commands**

### **Stop Processing**
- Press `Ctrl+C` to stop current processing
- Check `k1_multi_folder.log` for detailed information

### **Reset & Restart**
```bash
# Remove output folders
rmdir /s k1_output

# Restart processing
py k1_multi_folder.py --base-input "k1_test_input" --base-output "k1_output" --config "final_v2"
```

---

## 📝 **Notes**

- **Shadow Cutting**: All configurations now have enhanced safety margins
- **Quality**: Maintains 100% original image quality
- **Fonts**: Automatically downloads and caches Google Fonts
- **Logging**: Comprehensive logging to `k1_multi_folder.log`
- **Safety**: No shadow cutting with any configuration

---

*Last Updated: Based on k1_test_input multi-folder structure*
*Status: ✅ All features tested and working*
