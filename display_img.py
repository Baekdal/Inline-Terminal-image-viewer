def display(img, pixel_width=400, method='sixel', term_width=80):
	# accept file path or PIL Image
	if isinstance(img, (str, bytes)):
		img = Image.open(img)
	img = img.convert("RGB")

	if method == "halfblock":
		width, height = img.size
		term_height   = int((height / width) * term_width * 0.5)
		if term_height % 2 != 0:
			term_height += 1

		img    = img.resize((term_width, term_height * 2), Image.LANCZOS)
		pixels = img.load()

		for row in range(term_height):
			line = []
			for col in range(term_width):
				fr, fg, fb = pixels[col, row * 2]
				br, bg, bb = pixels[col, row * 2 + 1]
				line.append(f"\x1b[38;2;{fr};{fg};{fb}m\x1b[48;2;{br};{bg};{bb}m▀")
			print("".join(line) + "\033[0m")

	elif method == "sixel":
		width, height = img.size
		pixel_height  = int((height / width) * pixel_width)
		img           = img.resize((pixel_width, pixel_height), Image.LANCZOS)

		quantized   = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
		palette_raw = quantized.getpalette()

		index_arr = np.frombuffer(quantized.tobytes(), dtype=np.uint8).reshape(pixel_height, pixel_width)

		ESC = "\033"
		DCS = ESC + "P"
		ST  = ESC + "\\"

		out = []
		out.append(DCS + '7;1;q"1;1')

		for i in range(256):
			r, g, b = palette_raw[i*3], palette_raw[i*3+1], palette_raw[i*3+2]
			out.append(f"#{i};2;{round(r*100/255)};{round(g*100/255)};{round(b*100/255)}")

		bands       = (pixel_height + 5) // 6
		bit_weights = np.array([1, 2, 4, 8, 16, 32], dtype=np.uint8)
		all_colors  = np.arange(256, dtype=np.uint8)
		chr_table   = [chr(i) for i in range(256)]

		for band in range(bands):
			y_start = band * 6
			y_end   = min(y_start + 6, pixel_height)
			rows    = y_end - y_start

			band_indices = index_arr[y_start:y_end]

			presence = (band_indices[:, :, np.newaxis] == all_colors)
			bits     = (presence * bit_weights[:rows, np.newaxis, np.newaxis]).sum(axis=0).T.astype(np.uint8)
			used     = np.where(bits.any(axis=1))[0]

			first = True
			for color_idx in used:
				if not first:
					out.append("$")
				first = False
				out.append(f"#{color_idx}")

				row_vals  = bits[color_idx].tolist()
				run_char  = None
				run_count = 0
				parts     = []
				for val in row_vals:
					ch = chr_table[val + 63]
					if ch == run_char:
						run_count += 1
					else:
						if run_char is not None:
							parts.append(f"!{run_count}{run_char}" if run_count > 3 else run_char * run_count)
						run_char  = ch
						run_count = 1
				if run_char is not None:
					parts.append(f"!{run_count}{run_char}" if run_count > 3 else run_char * run_count)
				out.append("".join(parts))

			out.append("-")

		out.append(ST)
		sys.stdout.write("".join(out))
		sys.stdout.flush()
		print()


# # --- usage ---

# display("image.jpg")
# display("image.jpg", pixel_width=800)
# display("image.jpg", method="halfblock")

# # also works with an already-opened PIL image
# img = Image.open("image.jpg")
# display(img, pixel_width=400)
