import pygame
import typing


class EventHandler:
    def __init__(self) -> None:
        self.events = []
        self.mouse_rel = (0, 0)

        self._keypressed_callbacks: dict[int, list[typing.Callable]] = {}
        self._keydown_callbacks: dict[int, list[typing.Callable]] = {}
        self._keyup_callbacks: dict[int, list[typing.Callable]] = {}

        self._buttonpressed_callbacks: dict[int, list[typing.Callable]] = {}
        self._buttondown_callbacks: dict[int, list[typing.Callable]] = {}
        self._buttonup_callbacks: dict[int, list[typing.Callable]] = {}

        self._mouse_move_callbacks: list[typing.Callable[[tuple[int, int]], None]] = []

        self._quit_callbacks: list[typing.Callable] = []

    def register_keypressed_callback(self,
                                     key: int,
                                     callback: typing.Callable) -> None:
        """Registers a callback to be called when the key is pressed."""

        if key not in self._keypressed_callbacks:
            self._keypressed_callbacks[key] = []
        self._keypressed_callbacks[key].append(callback)

    def register_keydown_callback(self,
                                  key: int,
                                  callback: typing.Callable) -> None:
        """Registers a callback to be called when the key is down."""

        if key not in self._keydown_callbacks:
            self._keydown_callbacks[key] = []
        self._keydown_callbacks[key].append(callback)

    def register_keyup_callback(self,
                                key: int,
                                callback: typing.Callable) -> None:
        """Registers a callback to be called when the key is up."""
        if key not in self._keyup_callbacks:
            self._keyup_callbacks[key] = []
        self._keyup_callbacks[key].append(callback)

    def register_buttonpressed_callback(self,
                                        button: int,
                                        callback: typing.Callable) -> None:
        """Registers a callback to be called when the button is pressed."""
        if button-1 not in self._buttonpressed_callbacks:
            self._buttonpressed_callbacks[button-1] = []
        self._buttonpressed_callbacks[button-1].append(callback)

    def register_buttondown_callback(self,
                                     button: int,
                                     callback: typing.Callable) -> None:
        """Registers a callback to be called when the button is down."""
        if button not in self._buttondown_callbacks:
            self._buttondown_callbacks[button] = []
        self._buttondown_callbacks[button].append(callback)

    def register_buttonup_callback(self,
                                   button: int,
                                   callback: typing.Callable) -> None:
        """Registers a callback to be called when the button is up."""
        if button not in self._buttonup_callbacks:
            self._buttonup_callbacks[button] = []
        self._buttonup_callbacks[button].append(callback)

    def register_mouse_move_callback(self,
                                     callback: typing.Callable[[tuple[int, int]], None]) -> None:
        """Registers a callback to be called when the cursor is dragging."""
        self._mouse_move_callbacks.append(callback)

    def register_quit_callback(self,
                               callback: typing.Callable) -> None:
        """Registers a callback to be called when the game is quit."""
        self._quit_callbacks.append(callback)

    def handle_events(self) -> None:
        """Handles all events."""
        self.events = pygame.event.get()
        self.mouse_rel = pygame.mouse.get_rel()

        for event in self.events:
            if event.type == pygame.QUIT:
                self._quit()
                continue

            if event.type == pygame.KEYDOWN:
                self._keydown(event.key)
                continue

            if event.type == pygame.KEYUP:
                self._keyup(event.key)
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                self._buttondown(event.button)
                continue

            if event.type == pygame.MOUSEBUTTONUP:
                self._buttonup(event.button)
                continue

            if event.type == pygame.MOUSEMOTION:
                self._mouse_move()

        key_pressed = pygame.key.get_pressed()
        button_pressed = pygame.mouse.get_pressed(5)

        for key in self._keypressed_callbacks:
            if key_pressed[key]:
                self._keypressed(key)

        for button in self._buttonpressed_callbacks:
            if button_pressed[button]:
                self._buttonpressed(button)

    def _keypressed(self,
                    key: int) -> None:
        """Calls all callbacks registered to the key pressed."""
        if key not in self._keypressed_callbacks:
            return

        for callback in self._keypressed_callbacks[key]:
            callback()

    def _keydown(self,
                 key: int) -> None:
        """Calls all callbacks registered to the key down."""
        if key not in self._keydown_callbacks:
            return

        for callback in self._keydown_callbacks[key]:
            callback()

    def _keyup(self,
               key: int) -> None:
        """Calls all callbacks registered to the key leave."""
        if key not in self._keyup_callbacks:
            return

        for callback in self._keyup_callbacks[key]:
            callback()

    def _buttonpressed(self,
                       button: int) -> None:
        """Calls all callbacks registered to the button pressed."""
        if button not in self._buttonpressed_callbacks:
            return

        for callback in self._buttonpressed_callbacks[button]:
            callback()

    def _buttondown(self,
                    button: int) -> None:
        """Calls all callbacks registered to the button down."""
        if button not in self._buttondown_callbacks:
            return

        for callback in self._buttondown_callbacks[button]:
            callback()

    def _buttonup(self,
                  button: int) -> None:
        """Calls all callbacks registered to the button up."""
        if button not in self._buttonup_callbacks:
            return

        for callback in self._buttonup_callbacks[button]:
            callback()

    def _mouse_move(self) -> None:
        """Calls all callbacks registered to the mouse move."""
        for callback in self._mouse_move_callbacks:
            callback(self.mouse_rel)

    def _quit(self) -> None:
        """Calls all callbacks registered to the quit event."""
        for callback in self._quit_callbacks:
            callback()
