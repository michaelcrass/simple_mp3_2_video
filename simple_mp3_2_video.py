import os
import subprocess

def list_files_by_ext(folder, exts):
    files = [f for f in os.listdir(folder) if f.lower().endswith(exts)]
    for i, f in enumerate(files, 1):
        print(f"[{i}] {f}")
    return files

def choose_file(files, prompt):
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(files):
                return files[choice - 1]
        except ValueError:
            pass
        print("Invalid choice, try again.")

def concat_mp3s(mp3_1, mp3_2, output_file):
    with open("input.txt", "w") as f:
        f.write(f"file '{mp3_1}'\n")
        f.write(f"file '{mp3_2}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "input.txt",
        "-c", "copy", output_file
    ], check=True)
    os.remove("input.txt")



def create_video(image_path, audio_path, output_path):
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-c:v", "mpeg4",                # <- use mpeg4 instead of libx264
        "-q:v", "3",                    # quality setting for mpeg4
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-vf", "scale=1920:1080",
        output_path
    ], check=True)


def main():
    folder = "."

    print("Choose an image file:")
    images = list_files_by_ext(folder, (".jpg", ".jpeg", ".png"))
    img_file = choose_file(images, "Select image [1-{}]: ".format(len(images)))

    print("\nChoose first MP3 file:")
    mp3s = list_files_by_ext(folder, (".mp3",))
    mp3_file1 = choose_file(mp3s, "Select first MP3 [1-{}]: ".format(len(mp3s)))

    print("\nChoose second MP3 file:")
    mp3_file2 = choose_file(mp3s, "Select second MP3 [1-{}]: ".format(len(mp3s)))

    combined_audio = "combined_audio.mp3"
    output_video = "output_video.mp4"

    print("\n🔄 Concatenating audio...")
    concat_mp3s(mp3_file1, mp3_file2, combined_audio)

    print("🎞️  Creating video...")
    create_video(img_file, combined_audio, output_video)

    print(f"\n✅ Done! Saved to: {output_video}")
    os.remove(combined_audio)

if __name__ == "__main__":
    main()
