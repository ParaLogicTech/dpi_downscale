from PIL import Image
from tkinter import Tk, HORIZONTAL
from tkinter.ttk import Progressbar, Label
import os
import sys

Image.MAX_IMAGE_PIXELS = 933120000

DOWNSCALED_DIRECTORY = "downscaled"
PROGRAM_DIRECTORY = os.path.dirname(os.path.realpath(sys.argv[0]))
DOWNSCALED_PATH = os.path.join(PROGRAM_DIRECTORY, DOWNSCALED_DIRECTORY)

DOWNSCALED_DPI = 10
JPEG_QUALITY = 70

root = Tk(className=" Downscaling Images")
progress_bar = Progressbar(root, orient=HORIZONTAL, length=800, mode='determinate')
progress_label = Label(root, text="Downscaling")
error_label = Label(root, text="")


def main():
	progress_bar['value'] = 0

	progress_bar.pack(padx=10, pady=10)
	progress_label.pack(padx=10, pady=10)
	error_label.pack(padx=10, pady=10)

	root.update_idletasks()
	root.after_idle(start_downscale)
	root.mainloop()


def start_downscale():
	if sys.argv and len(sys.argv) > 1:
		file_list = sys.argv[1:]
	else:
		file_list = get_files()

	root.update_idletasks()
	downscale_multiple_files(file_list)


def downscale_multiple_files(file_list):
	count = len(file_list)
	completed = 0
	for i, file in enumerate(file_list):
		update_progress(file, i, count)
		success = downscale_file(file)

		if success:
			completed += 1

	handle_completed(completed, count)


def update_progress(file, i, count):
	percentage = round(i / count * 100, 0)
	progress_bar['value'] = int(percentage)

	progress_text = f"({i+1}/{count}) {file}"
	progress_label['text'] = progress_text

	root.update_idletasks()


def handle_completed(completed, count):
	progress_bar['value'] = 100

	progress_text = f"({completed}/{count}) Downscaled"
	progress_label['text'] = progress_text

	root.update_idletasks()

	if completed == count:
		root.quit()


def downscale_file(file):
	pwd = os.getcwd()

	filename = os.path.splitext(os.path.basename(file))[0]
	downscaled_file = os.path.join(DOWNSCALED_PATH, f"{filename}.jpg")

	# if os.path.isfile(downscaled_file):
	# 	return

	try:
		im = Image.open(os.path.join(pwd, file))

		if im.mode == "RGBA":
			im = im.convert("RGB")

		dpi = im.info['dpi']
		out_resolution = tuple(int(im.size[i] / dpi[i] * DOWNSCALED_DPI) for i in range(2))

		im.thumbnail(out_resolution)

		create_downscaled_directory()
		im.save(downscaled_file, "JPEG", quality=JPEG_QUALITY, dpi=(DOWNSCALED_DPI, DOWNSCALED_DPI))
	except Exception as e:
		error_label['text'] = f"({file}) {e}"
		root.update_idletasks()
		return False

	return True


def get_files():
	pwd = os.getcwd()

	all_files = [file for file in os.listdir(pwd) if os.path.isfile(os.path.join(pwd, file))]

	files = []
	for file in all_files:
		ext = os.path.splitext(os.path.join(pwd, file))[1].lower()
		if ext in (".tiff", ".tif"):
			files.append(file)

	return files


def create_downscaled_directory():
	if not os.path.exists(DOWNSCALED_PATH):
		os.makedirs(DOWNSCALED_PATH)
		return True


if __name__ == '__main__':
	main()
