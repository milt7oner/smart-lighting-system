from src.utils.model_exporter import ModelExporter

exporter = ModelExporter("yolov8n.pt")

# Export to TFLite INT8
exported_path = exporter.export_tflite(int8=True)

# Compare sizes
sizes = exporter.compare_sizes()

print("\n── MODEL EXPORT REPORT ─────────────────")
print(f"Original (.pt)     : {sizes['original_pt']} MB")
print(f"TFLite INT8        : {sizes['tflite_int8']} MB")

if sizes['tflite_int8']:
    reduction = ((sizes['original_pt'] - sizes['tflite_int8']) / sizes['original_pt']) * 100
    print(f"Size reduction     : {reduction:.1f}%")
print("────────────────────────────────────────\n")