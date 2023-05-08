from PIL import Image
from tkinter import Tk, HORIZONTAL
from tkinter.ttk import Progressbar, Label
import os
import sys

Image.MAX_IMAGE_PIXELS = 933120000

PWD = os.getcwd()
PROGRAM_DIRECTORY = os.path.dirname(os.path.realpath(sys.argv[0]))

DOWNSCALED_DIRECTORY = "downscaled"

DOWNSCALED_DPI = 10
JPEG_QUALITY = 75

root = Tk(className=" Downscaling Images")
progress_bar = Progressbar(root, orient=HORIZONTAL, length=700, mode='determinate')
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

		expanded_list = []
		for file in file_list:
			if os.path.isdir(file):
				expanded_list += get_files(file)
			else:
				expanded_list.append(file)
	else:
		file_list = get_files()
		expanded_list = file_list

	downscale_multiple_files(expanded_list)


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
	filename = os.path.splitext(os.path.basename(file))[0]

	root_directory = os.path.dirname(file)
	downscaled_file = os.path.join(root_directory, DOWNSCALED_DIRECTORY, f"{filename}.jpg")

	# if os.path.isfile(downscaled_file):
	# 	return

	try:
		im = Image.open(file)

		if im.mode == "RGBA":
			im = im.convert("RGB")

		dpi = im.info['dpi']
		out_resolution = tuple(int(im.size[i] / dpi[i] * DOWNSCALED_DPI) for i in range(2))

		im.thumbnail(out_resolution)

		create_missing_directory(downscaled_file)
		im.save(downscaled_file, "JPEG", quality=JPEG_QUALITY, dpi=(DOWNSCALED_DPI, DOWNSCALED_DPI))
	except Exception as e:
		error_label['text'] = f"({file}) {e}"
		root.update_idletasks()
		return False

	return True


def get_files(root_directory=None):
	if not root_directory:
		root_directory = PWD

	all_files = [file for file in os.listdir(root_directory) if os.path.isfile(os.path.join(root_directory, file))]

	files = []
	for file in all_files:
		file_path = os.path.join(root_directory, file)
		ext = os.path.splitext(file_path)[1].lower()
		if ext in (".tiff", ".tif"):
			files.append(file_path)

	return files


def create_missing_directory(path):
	directory = os.path.dirname(path)
	if not os.path.exists(directory):
		os.makedirs(directory)
		return True


if __name__ == '__main__':
	main()
