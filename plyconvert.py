import struct
import argparse
import os

def extract_ply_header(filepath):
    with open(filepath, 'rb') as f:
        header_lines = []
        while True:
            line = f.readline()
            header_lines.append(line)
            if b'end_header' in line:
                break
        header = b''.join(header_lines)
        data_start = f.tell()
    return header, data_start

def count_vertex_properties(header):
    return sum(1 for line in header.decode().splitlines() if line.startswith("property float"))

def update_vertex_count_in_header(header_bytes, new_count):
    lines = header_bytes.decode().splitlines()
    updated_lines = []
    for line in lines:
        if line.startswith("element vertex"):
            updated_lines.append(f"element vertex {new_count}")
        else:
            updated_lines.append(line)
    return '\n'.join(updated_lines).encode() + b'\n'

def patch_gut_ply_with_normals(original_ply_path, gut_ply_path, output_ply_path):
    print("🔧 Reading headers...")
    header_unity, _ = extract_ply_header(original_ply_path)
    header_gut, offset_gut = extract_ply_header(gut_ply_path)

    num_props_unity = count_vertex_properties(header_unity)
    num_props_gut = count_vertex_properties(header_gut)

    float_size = 4
    vertex_size_gut = num_props_gut * float_size
    vertex_size_unity = num_props_unity * float_size
    num_dummy_normals = num_props_unity - num_props_gut

    if num_dummy_normals != 3:
        raise ValueError(f"❌ Format mismatch: Expected exactly 3 missing values for normals, but found {num_dummy_normals}.")

    with open(gut_ply_path, 'rb') as f:
        f.seek(offset_gut)
        gut_data = f.read()

    num_vertices = len(gut_data) // vertex_size_gut
    print(f"📦 Detected {num_vertices} vertices in 3DGUT file.")

    # Unpack the float data
    gut_floats = struct.unpack('<' + 'f' * (num_vertices * num_props_gut), gut_data)

    # Patch each vertex with dummy normals
    patched_floats = []
    for i in range(num_vertices):
        start = i * num_props_gut
        end = (i + 1) * num_props_gut
        vertex = gut_floats[start:end]
        patched_vertex = vertex[:3] + (0.0, 0.0, 0.0) + vertex[3:]
        patched_floats.extend(patched_vertex)

    # Update header with correct vertex count
    corrected_header = update_vertex_count_in_header(header_unity, num_vertices)

    # Write to output file
    print(f"💾 Writing patched file to: {output_ply_path}")
    with open(output_ply_path, 'wb') as f:
        f.write(corrected_header)
        f.write(struct.pack('<' + 'f' * len(patched_floats), *patched_floats))

    print("✅ Done. The patched file is now Unity-compatible.")

# === Entry point ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patch 3DGUT PLY by inserting dummy normals to match Unity Gaussian Splatting format.")
    parser.add_argument('model_name', help='Name of the model to modify (without extension)')

    args = parser.parse_args()

    # Define paths
    original_ply = 'reference.ply'
    gut_ply = f'{args.model_name}.ply'
    output_ply = f'patched_{args.model_name}.ply'

    patch_gut_ply_with_normals(original_ply, gut_ply, output_ply)
