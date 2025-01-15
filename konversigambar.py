from PIL import Image
import os

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_message):
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
    return message

def encode_image(input_image, secret_message):
    try:
        img = Image.open(input_image)
        binary_message = text_to_binary(secret_message) + '1111111111111110'
        img_data = iter(img.getdata())

        new_pixels = []
        for pixel in img_data:
            if len(binary_message) > 0:
                new_pixel = []
                for value in pixel[:3]:
                    if len(binary_message) > 0:
                        new_pixel.append(value & ~1 | int(binary_message[0]))
                        binary_message = binary_message[1:]
                    else:
                        new_pixel.append(value)
                new_pixels.append(tuple(new_pixel + list(pixel[3:])))
            else:
                new_pixels.append(pixel)

        img.putdata(new_pixels)
        return img

    except Exception as e:
        print(f"Error: {e}")
        return None

def decode_image(input_image):
    try:
        img = Image.open(input_image)
        img_data = iter(img.getdata())

        binary_message = ''
        for pixel in img_data:
            for value in pixel[:3]:
                binary_message += str(value & 1)

        message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if byte == '11111111':
                break
            message += chr(int(byte, 2))

        return message

    except Exception as e:
        print(f"Error: {e}")
        return None

def validate_file_path(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return file_path

def validate_output_path(output_path):
    if not output_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        raise ValueError("Output file name must include a valid image extension (e.g., .png, .jpg)")
    return output_path

if __name__ == "__main__":
    print("--- Steganografi: Encode/Decode Pesan dalam Gambar ---")
    while True:
        print("Pilih opsi:")
        print("1. Encode pesan ke dalam gambar")
        print("2. Decode pesan dari gambar")
        print("3. Keluar")
        opsi = input("Masukkan pilihan: ")

        if opsi == '1':
            try:
                input_image_path = input("Enter the image path (e.g., input.png): ")
                validate_file_path(input_image_path)

                secret_message = input("Enter the secret message: ")
                output_image_path = input("Enter the output file name (e.g., output.png): ")
                validate_output_path(output_image_path)

                stego_image = encode_image(input_image_path, secret_message)

                if stego_image:
                    try:
                        stego_image.save(output_image_path)
                        print(f"Message embedded successfully! The new image is saved as {output_image_path}")
                    except Exception as save_error:
                        print(f"Failed to save image: {save_error}")
                else:
                    print("Encoding process failed.")

            except FileNotFoundError as fnf_error:
                print(fnf_error)
            except ValueError as val_error:
                print(val_error)
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif opsi == '2':
            try:
                input_image_path = input("Enter the image path (e.g., input.png): ")
                validate_file_path(input_image_path)

                secret_message = decode_image(input_image_path)
                if secret_message:
                    print(f"Message extracted successfully: {secret_message}")
                else:
                    print("Decoding process failed.")

            except FileNotFoundError as fnf_error:
                print(fnf_error)
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif opsi == '3':
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")