# Number Offset Feature Documentation

## Overview

The watermark scripts now support **X and Y offset positioning for number watermarks**, allowing precise control over where numbers appear on images. This feature works alongside the existing PNG watermark offset functionality.

## New Parameters

### Command Line Arguments

- `--number-x-offset`: Horizontal offset for number watermark position (can be negative)
- `--number-y-offset`: Vertical offset for number watermark position (can be negative)

### Default Values

Both parameters default to `0` (no offset), maintaining backward compatibility.

## How It Works

The number offset parameters are applied **after** the base position calculation. This means:

1. **Base Position**: Numbers are positioned according to `--number-position` and `--margin`
2. **Offset Application**: The X and Y offsets are then added to fine-tune the final position
3. **Final Position**: `final_x = base_x + number_x_offset`, `final_y = base_y + number_y_offset`

## Usage Examples

### Basic Number Offset Usage

```bash
# Move numbers 50 pixels to the right
python watermark_script.py \
  --input-folder "./photos" \
  --output-folder "./output" \
  --custom-text "mypage.com" \
  --enable-numbering \
  --number-x-offset 50

# Move numbers 30 pixels up (negative Y offset)
python watermark_script.py \
  --input-folder "./photos" \
  --output-folder "./output" \
  --custom-text "mypage.com" \
  --enable-numbering \
  --number-y-offset -30

# Combine both offsets
python watermark_script.py \
  --input-folder "./photos" \
  --output-folder "./output" \
  --custom-text "mypage.com" \
  --enable-numbering \
  --number-x-offset 100 \
  --number-y-offset -50
```

### With PNG Watermarks

```bash
# PNG watermark with number offsets
python watermark_script.py \
  --input-folder "./photos" \
  --output-folder "./output" \
  --png-watermark "./logo.png" \
  --enable-numbering \
  --number-x-offset 75 \
  --number-y-offset -25
```

### Using k1_multi_folder.py

```bash
# Override FINAL_V3 configuration with custom number offsets
python k1_multi_folder.py \
  --base-input "k1_test_input" \
  --base-output "k1_output" \
  --config "final_v3" \
  --number-x-offset 75 \
  --number-y-offset -25
```

## Configuration Integration

### FINAL_V3 Configuration

The FINAL_V3 configuration in `k1_multi_folder.py` now includes:

```python
"final_v3": {
    # ... existing parameters ...
    "number_x_offset": "0",                  # X offset for fine-tuning number position
    "number_y_offset": "0"                   # Y offset for fine-tuning number position
}
```

### Custom Settings Override

You can override these values when calling `k1_multi_folder.py`:

```bash
# Override configuration values
python k1_multi_folder.py \
  --base-input "k1_test_input" \
  --base-output "k1_output" \
  --config "final_v3" \
  --number-x-offset "100" \
  --number-y-offset "-50"
```

## Offset Behavior by Position

### Top-Left Position
- **Base**: `(margin + safety_margin, margin + safety_margin)`
- **With Offsets**: `(margin + safety_margin + x_offset, margin + safety_margin + y_offset)`

### Top-Right Position
- **Base**: `(img_width - number_width - margin - safety_margin, margin + safety_margin)`
- **With Offsets**: `(img_width - number_width - margin - safety_margin + x_offset, margin + safety_margin + y_offset)`

### Bottom-Left Position
- **Base**: `(margin + safety_margin, img_height - number_height - margin - safety_margin)`
- **With Offsets**: `(margin + safety_margin + x_offset, img_height - number_height - margin - safety_margin + y_offset)`

### Center Position
- **Base**: `((img_width - number_width) // 2, (img_height - number_height) // 2)`
- **With Offsets**: `((img_width - number_width) // 2 + x_offset, (img_height - number_height) // 2 + y_offset)`

### Bottom-Right Position (Default)
- **Base**: `(img_width - number_width - margin - safety_margin, img_height - number_height - margin - safety_margin)`
- **With Offsets**: `(img_width - number_width - margin - safety_margin + x_offset, img_height - number_height - margin - safety_margin + y_offset)`

## Practical Use Cases

### 1. **Avoiding Overlaps**
When numbers might overlap with other elements:
```bash
--number-x-offset 50    # Move numbers away from center text
--number-y-offset -30   # Move numbers up to avoid bottom elements
```

### 2. **Brand Positioning**
Fine-tune number placement for specific brand requirements:
```bash
--number-x-offset 100   # Move numbers to specific horizontal position
--number-y-offset 0     # Keep vertical position unchanged
```

### 3. **Layout Adjustments**
Compensate for different image aspect ratios:
```bash
--number-x-offset -25   # Move numbers left for wide images
--number-y-offset 20    # Move numbers down for tall images
```

### 4. **Print Preparation**
Ensure numbers are positioned correctly for printing:
```bash
--number-x-offset 75    # Move numbers to safe print area
--number-y-offset -50   # Move numbers up from bottom edge
```

### 5. **Right-Alignment Consistency**
Ensure numbers with different widths align properly on the right:
```bash
# Before fix: Numbers like "1111" and "0000" would not align properly
# After fix: All numbers now align perfectly on their right edge
--number-position "bottom-right"    # Use right-aligned positioning
--number-x-offset -20               # Fine-tune horizontal position
--number-y-offset -120              # Fine-tune vertical position
```

**Example**: With `--number-position "bottom-right"`:
- `1111` (wider number) → positioned so right edge is at margin
- `0000` (narrower number) → positioned so right edge is at same margin
- `9999` (wider number) → positioned so right edge is at same margin
- Result: All numbers align perfectly on their right edge

## Testing the Feature

Use the included test script to verify functionality:

```bash
python test_number_offsets.py
```

This will create multiple output folders demonstrating different offset combinations.

## Technical Details

### Implementation
- Offsets are applied in the `_calculate_number_position()` method
- All position calculations now include offset parameters
- Offsets work with all number positions and margin settings
- Safety margins for shadow effects are preserved
- **Fixed**: Number watermark positions are now properly calculated and applied using the `_calculate_watermark_positions()` method
- **Enhanced**: Right-aligned positions now use the actual number width for proper alignment

### Right-Alignment Fix
**Problem**: When using right-aligned positions (`top-right`, `bottom-right`), numbers with different widths (like `1111` vs `0000`) were not properly aligned because they were positioned based on their left edge.

**Solution**: The positioning logic now:
1. Creates the number watermark first to get its actual dimensions
2. Uses the **right edge** of the number as the reference point for right-aligned positions
3. Ensures all numbers align properly regardless of their width

**Result**: Numbers like `1111`, `0000`, `9999`, etc. now all align perfectly on their right edge when using right-aligned positions.

### Safety Features
- Offsets can be negative (moving left/up)
- Offsets are applied after safety margin calculations
- No risk of numbers being cut off due to offsets
- Maintains compatibility with existing shadow and blur effects
- Right-aligned numbers maintain consistent positioning regardless of width

### Performance Impact
- Minimal performance impact (simple addition operations)
- No additional image processing required
- Offsets are calculated once per image

## Troubleshooting

### Common Issues

1. **Numbers appear cut off**
   - Reduce offset values
   - Check image dimensions
   - Verify margin settings

2. **Unexpected positioning**
   - Verify offset values are correct
   - Check number position setting
   - Test with zero offsets first

3. **Performance issues**
   - Offsets have minimal impact
   - Check other parameters first
   - Verify image sizes

4. **Number offsets not working (FIXED)**
   - **Issue**: Number watermarks were ignoring offset parameters due to position recalculation in `process_image()`
   - **Solution**: Fixed to use calculated positions from `_calculate_watermark_positions()` method
   - **Status**: ✅ RESOLVED - Number offsets now work correctly in both `watermark_script.py` and `k1_multi_folder.py`

5. **Right-aligned numbers not aligning properly (FIXED)**
   - **Issue**: Numbers with different widths (like `1111` vs `0000`) were not properly aligned when using right-aligned positions
   - **Solution**: Modified positioning logic to use the actual number width and right edge as reference point
   - **Status**: ✅ RESOLVED - All numbers now align perfectly on their right edge regardless of width

### Debug Tips

- Use `--dry-run` to see what would be processed
- Start with small offset values (10-20 pixels)
- Test with different number positions
- Verify results in output folders
- Check that command includes `--number-x-offset` and `--number-y-offset` parameters

## Future Enhancements

Potential improvements for future versions:
- **Relative offsets** (percentage-based positioning)
- **Smart positioning** (automatic overlap detection)
- **Preset configurations** (common offset combinations)
- **Visual preview** (offset effect simulation)

---

## Summary

The new number offset feature provides precise control over number watermark positioning while maintaining full backward compatibility. Use it to:

- **Fine-tune** number placement for specific layouts
- **Avoid overlaps** with other watermarks or image elements  
- **Optimize positioning** for different image types and sizes
- **Maintain consistency** across varied image collections

The feature integrates seamlessly with existing functionality and can be easily adopted in existing workflows.
