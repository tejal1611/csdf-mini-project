import hashlib
from PIL import Image
from PIL.ExifTags import TAGS
import os


# Function to compute SHA-256 hash of an image
def compute_sha256(image_path):
    with open(image_path, "rb") as f:
        bytes = f.read()  # Read the image data as bytes
        sha256_hash = hashlib.sha256(bytes).hexdigest()
    return sha256_hash


# Function to extract metadata from the image
def extract_metadata(image_path):
    image = Image.open(image_path)
    metadata = {}
    if hasattr(image, '_getexif'):  # Check if the image has EXIF metadata
        exifdata = image._getexif()
        if exifdata is not None:
            for tag_id, value in exifdata.items():
                tag_name = TAGS.get(tag_id, tag_id)
                metadata[tag_name] = value
    return metadata


# Function to save metadata and hash to a file
def save_metadata_and_hash(image_path, output_file):
    metadata = extract_metadata(image_path)
    image_hash = compute_sha256(image_path)

    with open(output_file, "w") as f:
        f.write("Metadata:\n")
        for tag, value in metadata.items():
            f.write(f"{tag}: {value}\n")

        f.write("\nSHA-256 Hash:\n")
        f.write(image_hash)

    print(f"Metadata and hash saved to {output_file}")


# Function to compare new image with saved hash
def compare_image_with_hash(image_path, old_hash_file):
    # Compute hash of the new image
    new_image_hash = compute_sha256(image_path)

    # Load old hash from the saved file
    with open(old_hash_file, 'r') as f:
        lines = f.readlines()
        old_image_hash = lines[-1].strip()  # The hash is the last line in the file

    # Compare hashes
    if new_image_hash == old_image_hash:
        print("The image is not corrupted or tampered with.")
    else:
        print("The image has been tampered with or corrupted.")


# Example usage
if __name__ == "__main__":
    original_image = "i1.jpeg"  # Path to the original image
    hash_file = "op.txt"  # File to store metadata and hash
    new_image = "i1.jpeg"  # Path to the new image to compare

    # First, save metadata and hash for the original image
    save_metadata_and_hash(original_image, hash_file)

    # Later, compare a new image with the saved hash
    compare_image_with_hash(new_image, hash_file)  

    #new commit
 
    
    #gkstnl