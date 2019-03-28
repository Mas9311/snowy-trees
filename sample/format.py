class Notification:
    """Prints a Notification to the Terminal, so don't print it yourself.
    The message is surrounded with characters to help it stand out.
    The only parameter is a message/list of messages:
      - The first (or only) message is the title.
      - Optional: You can add additional messages in input
        - Prints in the body block of the Notification.
    Title message is centered, body messages are left-justified"""
    def __init__(self, messages):
        self.default_len = 20
        self.max_len = self.default_len

        self.title_side = '▓'
        self.title_top = '▔'
        self.title_bot = '▁'
        self.body_char = '░'

        self.messages = messages
        self.title_m = None
        self.body_ms = None

        self.title = None
        self.body = None
        self.create()

        print(self)

    def create(self):
        """Only called once (during initialization).
        Prepares the class variables before printing."""
        self.set_messages()
        self.set_max()
        self.center_title()
        self.create_title()
        self.create_body()

    def set_messages(self):
        """Assigns the title and body messages from the input, messages.
        If input is only one item, converts it to a list.
        Strips whitespaces from title and body.
        If title is odd: make it even by adding a space."""
        self.messages = self.messages if isinstance(self.messages, list) else [self.messages]

        self.body_ms = []
        for i, message in enumerate(self.messages):
            message = str(message).strip()
            if i is 0:
                self.title_m = message
            else:
                self.body_ms.append(message)

    def set_max(self):
        """Finds the maximum length of any messages in the list."""
        for i, line in enumerate(self.messages):
            line_len = len(line) + 4
            line_len += 2 if i is 0 else 0  # Extra padding for the Title
            self.max_len = max(self.max_len, line_len)

    def center_title(self):
        """In the case of:
            One of the body message lines are the longest,
            That body message line is of an odd-number length
            and the title message length is an even number,
        Then:
            Center the title message by increasing the max_len by 1."""
        if self.max_len % 2 is 1 and len(self.title_m) % 2 is 0:
            # print('center the title')
            self.max_len += 1

    def create_title(self):
        top = f'{self.title_side}{self.title_top * (self.max_len - 2)}{self.title_side}\n'
        mid = self.message_line(self.title_m, True)
        bot = f'{self.title_side}{self.title_bot * (self.max_len - 2)}{self.title_side}\n'
        self.title = (f'{top}'
                      f'{mid}'
                      f'{bot}')

    def create_body(self):
        """If the length of the messages is > 1,
        Create the body (the bottom half) of the Notification.
         - Includes a blank line, all body messages, another blank line, and the bottom border."""
        if self.body_ms:
            self.body = self.blank()
            for message in self.body_ms:
                self.body += self.message_line(message)
            self.body += self.blank()
            self.body += self.full_line()

    def full_line(self, is_title=False, is_top=False):
        """Return a full line of characters.
        Three different lines can be returned from this:
          1. Top of the title box.
          2. Bottom of the title box.
          3. Bottom of the Notification box (if it has a body)."""
        if not is_title:
            side = char = self.body_char
        else:
            side = self.title_side
            char = self.title_top if is_top else self.title_bot
        return f'{side}{char * (self.max_len - 2)}{side}'

    def blank(self):
        """Returns a line of spaces surrounded by the body character of the l/r side.
        These will be printed above and below the body messages block
        to help the body messages stand out a little. Easier to read."""
        spaces = ' ' * (self.max_len - 2)
        return f'{self.body_char}{spaces}{self.body_char}\n'

    def message_line(self, message, is_title=False):
        """Returns a line that includes text surrounded by the border character
        on the l/r side. Title is centered, body messages are left-justified."""
        if is_title:  # Title message is centered
            left = right = ' ' * ((self.max_len - len(message) - 2) // 2)
            char = self.title_side
        else:  # Body messages are left-justified
            left = ' '
            right = ' ' * (self.max_len - len(message) - 3)
            char = self.body_char

        return f'{char}{left}{message}{right}{char}\n'

    def __str__(self):
        """Printable form of the class.
        This method is called in constructor, so do not save the Notification variable
        and no need to print(Notification)."""
        return(f'{self.title}'
               f'{self.body}')
