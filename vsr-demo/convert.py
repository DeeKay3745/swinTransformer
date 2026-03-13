import imageio

reader = imageio.get_reader("public/lip_detect.avi")
fps = reader.get_meta_data()["fps"]

writer = imageio.get_writer(
    "public/lip_detect.mp4",
    fps=fps,
    codec="libx264"
)

for frame in reader:
    writer.append_data(frame)

writer.close()

print("Video converted successfully")