from PIL import Image, ImageDraw, ImageFont

from src.data_sources.errors import BackgroundImageNotFoundError, UserImageNotFoundError
from src.repositories.code_time_data_repository import CodeTimeDataRepository
from src.use_cases.image_creator.base_image_creator import BaseImageCreator


class BasicImageCreator(BaseImageCreator):
    PROGRESS_BAR_WIDTH = 800
    PROGRESS_BAR_HEIGHT = 20
    USER_IMAGE_SIZE = 125

    def __init__(self, data_repository: CodeTimeDataRepository):
        super().__init__(data_repository)

    def create_image(self, statistics: dict):
        try:
            with Image.open(self.data_repository.get_file_from_setting("image")) as image:
                draw = ImageDraw.Draw(image)
                self.draw_title(draw, statistics["date"])
                self.draw_total_time(draw, statistics["total_time"])
                self.draw_activities(draw, statistics["activities"])
                self.draw_watermark(draw, image.height)
                self.paste_user_image(image)
                return image
        except FileNotFoundError:
            raise BackgroundImageNotFoundError()

    def paste_user_image(self, image):
        try:
            user_image = Image.open(self.data_repository.get_file_from_setting("user_image"), "r").convert("RGBA")
        except FileNotFoundError:
            raise UserImageNotFoundError()

        user_image = user_image.resize((BasicImageCreator.USER_IMAGE_SIZE, BasicImageCreator.USER_IMAGE_SIZE),
                                       Image.ANTIALIAS)

        user_image_x = image.width - BasicImageCreator.USER_IMAGE_SIZE - 140
        user_image_y = 200 - BasicImageCreator.USER_IMAGE_SIZE // 2
        image.paste(user_image, (user_image_x, user_image_y), user_image)

    def draw_watermark(self, draw: ImageDraw, max_height):
        username = self.data_repository.get_setting("username").strip()
        title = "by code-time"
        if username != "":
            title += f" for {username}"

        draw.text((140, max_height - 200), title, font=ImageFont.truetype(self.get_font("semi_bold"), 30),
                  fill=self.data_repository.get_setting("watermark_color"))

    def draw_activity(self, draw: ImageDraw, name: str, time: str, progress: float, x: int, y: int):
        title_font_size = 40
        text_progress_margin = 25

        progress_end_y = y + BasicImageCreator.PROGRESS_BAR_HEIGHT + text_progress_margin
        progress_start_xy = (x, y + text_progress_margin)

        background_end_xy = (x + BasicImageCreator.PROGRESS_BAR_WIDTH, progress_end_y)
        foreground_end_xy = (x + BasicImageCreator.PROGRESS_BAR_WIDTH * progress, progress_end_y)

        draw.rectangle((progress_start_xy, background_end_xy),
                       fill=self.data_repository.get_setting("progress_background_color"))
        draw.rectangle((progress_start_xy, foreground_end_xy),
                       fill=self.data_repository.get_setting("progress_foreground_color"))

        # Draw activity title
        draw.text((x, y - title_font_size), name,
                  font=ImageFont.truetype(self.get_font("semi_bold"), title_font_size),
                  fill=self.data_repository.get_setting("activity_title_color"))

        # Draw activity time
        draw.text((x + BasicImageCreator.PROGRESS_BAR_WIDTH, y - 20), BasicImageCreator.time_as_str(time),
                  font=ImageFont.truetype(self.get_font("bold"), 30),
                  fill=self.data_repository.get_setting("activity_time_color"),
                  anchor="rt")

    def draw_activities(self, draw: ImageDraw, activities: list):
        for i, activity in enumerate(activities):
            self.draw_activity(draw, activity["name"], activity["time"], activity["progress"], 140, 370 + i * 110)

    def draw_total_time(self, draw: ImageDraw, total_time):
        draw.text((140, 189), BasicImageCreator.time_as_str(total_time),
                  font=ImageFont.truetype(self.get_font("extra_bold"), 60),
                  fill=self.data_repository.get_setting("total_time_color"), )

    def draw_title(self, draw: ImageDraw, date: str):
        draw.text((140, 134), f"Coding statistics of {date}",
                  font=ImageFont.truetype(self.get_font("semi_bold"), 40),
                  fill=self.data_repository.get_setting("title_color"), )
