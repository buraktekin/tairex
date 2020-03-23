#! -*- coding: utf-8 -*-

"""
An interface to bridge python and browser to each other
through Selenium. By this, we could catch the responses
are fired by the game, during gameplay on the browser.
"""

# Interaction interface imports: Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# automatize detecting required webdriver version
from webdriver_manager.chrome import ChromeDriverManager
from params import GAME_URL
import time


class Interface(object):
    """Interface Module Implementation"""

    def __init__(self, conf=True):
        """Constructor"""

        # Create driver
        chrome_options = Options()
        chrome_options.add_argument('disable-infobars')
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            chrome_options=chrome_options
        )

        # set browser props
        self.driver.set_window_position(x=0, y=0)
        self.driver.set_window_size(300, 200)
        self.driver.get(GAME_URL)
        if conf:
            self.driver.execute_script(
                'Runner.config.ACCELERATION=0'
            )

        def restart(self) -> None:
            self.driver.execute_script(
                'Runner.instance_.restart()'
            )
            # put some delay here to
            # compansate game screen rendering
            time.sleep(5)

        def pause(self) -> None:
            return self.driver.execute_script(
                'return Runner.instance_.stop()'
            )

        def resume(self) -> None:
            return self.driver.execute_script(
                'return Runner.instance_.play()'
            )

        def close(self) -> None:
            self.driver.close()

        def jump(self) -> None:
            self.driver \
                .find_element_by_tag_name("body") \
                .send_keys(Keys.ARROW_UP)

        def duck(self) -> None:
            self.driver \
                .find_element_by_tag_name("body") \
                .send_keys(Keys.ARROW_DOWN)

        def get_score(self) -> int:
            # Weird but no prop returns the current score directly
            # Only option getting segments and concat them.
            score_segments = self.driver.execute_script(
                'return Runner.instance_.distanceMeter.digits'
            )  # returns list of score segments
            return int(''.join(score_segments))

        def is_dino_crashed(self) -> bool:
            return self.driver.execute_script(
                'return Runner.instance_.crashed'
            )

        def is_dino_running(self) -> bool:
            return self.driver.execute_script(
                'return Runner.instance_.playing'
            )


if __name__ == "__main__":
    Interface()
