def display_compare(*images, gap=20, gap_color=(30, 30, 30), pixel_width=800, method='sixel', term_width=80):
	# open any file paths
	imgs = []
	for img in images:
		if isinstance(img, (str, bytes)):
			img = Image.open(img)
		imgs.append(img.convert("RGB"))

	# scale all images to the same height as the first
	target_height = imgs[0].size[1]
	scaled = []
	for img in imgs:
		w, h   = img.size
		new_w  = int(w * target_height / h)
		scaled.append(img.resize((new_w, target_height), Image.LANCZOS))

	# build combined canvas
	total_width = sum(img.size[0] for img in scaled) + gap * (len(scaled) - 1)
	combined    = Image.new("RGB", (total_width, target_height), gap_color)

	x = 0
	for img in scaled:
		combined.paste(img, (x, 0))
		x += img.size[0] + gap

	display(combined, pixel_width=pixel_width, method=method, term_width=term_width)
