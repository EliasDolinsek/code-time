import sys

from PIL import Image, ImageDraw, ImageFont


class ImageCreator:
    PROGRESS_BAR_WIDTH = 800
    PROGRESS_BAR_HEIGHT = 20
    USER_IMAGE_SIZE = 100

    def __init__(self, config: dict):
        self.config = config
        self.font_paths = {
            "bold": "../assets/OpenSans-Bold.ttf",
            "extra_bold": "../assets/fonts/OpenSans-ExtraBold.ttf",
            "semi_bold": "../assets/fonts/OpenSans-SemiBold.ttf"
        }

    def paste_user_image(self, image):
        user_image = Image.open("../assets/user.png", "r")
        user_image = user_image.resize((ImageCreator.USER_IMAGE_SIZE, ImageCreator.USER_IMAGE_SIZE), Image.ANTIALIAS)
        image.paste(user_image,
                    (image.width - ImageCreator.USER_IMAGE_SIZE - 140, 200 - ImageCreator.USER_IMAGE_SIZE // 2), )

    def draw_watermark(self, draw: ImageDraw, max_height):
        draw.text((140, max_height - 200), "by code-time", font=ImageFont.truetype(self.font_paths["semi_bold"], 30),
                  fill=self.config["watermark_color"])

    def draw_activity(self, draw: ImageDraw, name: str, time: str, progress: float, x: int, y: int):
        title_font_size = 40
        text_progress_margin = 25

        progress_end_y = y + ImageCreator.PROGRESS_BAR_HEIGHT + text_progress_margin
        progress_start_xy = (x, y + text_progress_margin)

        background_end_xy = (x + ImageCreator.PROGRESS_BAR_WIDTH, progress_end_y)
        foreground_end_xy = (x + ImageCreator.PROGRESS_BAR_WIDTH * progress, progress_end_y)

        draw.rectangle((progress_start_xy, background_end_xy), fill=self.config["progress_background_color"])
        draw.rectangle((progress_start_xy, foreground_end_xy), fill=self.config["progress_foreground_color"])

        # Draw activity title
        draw.text((x, y - title_font_size), name,
                  font=ImageFont.truetype(self.font_paths["semi_bold"], title_font_size),
                  fill=self.config["activity_title_color"])

        # Draw activity time
        draw.text((x + ImageCreator.PROGRESS_BAR_WIDTH, y - 20), time,
                  font=ImageFont.truetype(self.font_paths["bold"], 30),
                  fill=self.config["activity_time_color"],
                  anchor="rt")

    def draw_activities(self, draw: ImageDraw, activities: list):
        for activity, index in zip(activities, range(len(activities))):
            self.draw_activity(draw, activity["name"], activity["time"], activity["progress"], 140, 370 + index * 110)

    def draw_total_time(self, draw: ImageDraw, total_time: str):
        draw.text((140, 189), total_time,
                  font=ImageFont.truetype(self.font_paths["extra_bold"], 60),
                  fill=self.config["total_time_color"], )

    def draw_title(self, draw: ImageDraw, date: str):
        draw.text((140, 134), f"Coding statistics of {date}",
                  font=ImageFont.truetype(self.font_paths["semi_bold"], 40),
                  fill=self.config["title_color"], )

    def create_image(self, statistics: dict):
        with Image.open(self.config["image"]) as image:
            draw = ImageDraw.Draw(image)
            self.draw_title(draw, statistics["date"])
            self.draw_total_time(draw, statistics["total_time"])
            self.draw_activities(draw, statistics["activities"])
            self.draw_watermark(draw, image.height)
            self.paste_user_image(image)


if __name__ == "__main__":
    config = {
        "title_color": (0, 0, 0, 255),
        "total_time_color": (0, 0, 0, 255),
        "progress_background_color": (0, 150, 199, 33),
        "progress_foreground_color": (0, 150, 199, 255),
        "activity_title_color": (0, 0, 0, 255),
        "activity_time_color": (0, 0, 0, 255),
        "watermark_color": (0, 0, 0, 255),
    }

    statistics = {
        "date": "5th Dec",
        "total_time": "5h 25min",
        "activities": [
            {
                "name": "PyCharm",
                "time": "5h 25min",
                "progress": 0.5
            },
            {
                "name": "IntelliJ",
                "time": "3h 42min",
                "progress": 0.3
            },
            {
                "name": "VS Code",
                "time": "3h 42min",
                "progress": 0.2
            },
            {
                "name": "Vim, X-Code and more",
                "time": "3h 42min",
                "progress": 0.1
            },
        ]
    }
    creator = ImageCreator("img1.png", config)
    creator.create_image(statistics)
